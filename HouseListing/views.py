import csv
from decimal import Decimal
from django.contrib.postgres.search import SearchVector
from django.db.models import Sum
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from HouseListing.models import Properties
from .forms import *
import datetime
from django.db.models import Q
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
import uuid
from django.core.mail import EmailMessage
from django.template import Context
from django.http import JsonResponse
from django.template.loader import get_template
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
# from authorizenet import apicontractsv1
# from authorizenet.apicontrollers import *
from decimal import *
from django.db.models.functions import TruncMonth

from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone



current_site = 'http://127.0.0.1:8000/'

current_site_online = 'https://aprilmanagement.pro'
# current_site_online = 'http://127.0.0.1:8000'

# listing views

# pending -> 0
# approved -> 1
# rejected -> 2


# sanitization algorithms

def sanitize(request):
    land_photos = PropertyImages.objects.filter(property__type__name='Land')

    for each_land in land_photos:
        each_land.home_tag = 'Others'
        each_land.save()
    return HttpResponse('sanitized')


def populateDbWithCities(request):
    locations = [
    "Westlands", "Karen", "Lavington", "Kileleshwa", "Runda", "Gigiri", "Parklands",
    "Hurlingham", "Langata", "South B", "South C", "Kilimani", "Upper Hill", "Nairobi West",
    "Donholm", "Embakasi", "Kasarani", "Roysambu", "Githurai", "Kahawa Wendani", "Ruiru",
    "Thika Road", "Muthaiga", "Ngong Road", "Eastleigh", "Umoja", "Buruburu", "Zimmerman",
    "Kariobangi", "Kayole", "Madaraka", "Pipeline", "Mlolongo", "Syokimau", "Ruaka",
    "Kangemi", "Komarock", "Kibera", "Mathare"
]

    for location in locations:
        try:
            Cities.objects.get(city_name=location)
        except:
            Cities.objects.create(city_name=location)

    return HttpResponse('worked')



def all_agents(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    
    all_users = UserProfile.objects.filter(user_account_type='LandLord')

    context = {
        'all_users': all_users,
    }
    return render(request, 'HouseListing/all_agents.html', context)


def all_cases(request):
    open_cases = LegalCase.objects.filter(case_open = True).order_by('-id')
    closed_cases = LegalCase.objects.filter(case_open = False).order_by('-id')

    context = {
        'open_cases': open_cases,
        'closed_cases': closed_cases,
    }
    return render(request, 'HouseListing/all_cases.html', context)

def agent_details ( request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    
    agent = UserProfile.objects.get(id=pk)

    active_properties_listings = Properties.objects.filter(user=agent.user, approved_by_admin=1, publish=True)
    off_market_properties = Properties.objects.filter(
            Q(user=request.user, managed_by_manyumba=False, approved_by_admin=0, publish=False) | 
            Q(user=request.user, managed_by_manyumba=False, approved_by_admin=True, publish=False)|
            Q(user=request.user, managed_by_manyumba=False, approved_by_admin=0, publish=True) |
            Q(user=request.user, managed_by_manyumba=False, approved_by_admin=2, publish=False) |
            Q(user=request.user, managed_by_manyumba=False, approved_by_admin=2, publish=True)
    )

    context = {
        'agent': agent,
        'active_properties_listings': active_properties_listings,
        'off_market_properties': off_market_properties,

    }

    return render(request, 'HouseListing/agents_details.html', context)




def listing_dashboard(request):

    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')

    approved_properties = Properties.objects.filter(user=request.user,managed_by_manyumba=False, approved_by_admin=1).count()
    pending_properties = Properties.objects.filter(user=request.user,managed_by_manyumba=False, approved_by_admin=0).count()
    active_listings = Properties.objects.filter(
        user=request.user, managed_by_manyumba=False, approved_by_admin=1, publish=True).count()
    off_market_properties = Properties.objects.filter(
        Q(user=request.user, managed_by_manyumba=False, approved_by_admin=0, publish=False) | Q(
            user=request.user, managed_by_manyumba=False, approved_by_admin=1, publish=False) | Q(user=request.user, managed_by_manyumba=False, approved_by_admin=0, publish=True)
    ).count()


    open_contracts = MaintenanceContract.objects.filter(super_admin_approved=True, open_for_bids=True).count()
    active_contracts = MaintenanceContract.objects.filter(selected_bid__business_owner__user = request.user ).count()

    all_contract = MaintenanceContract.objects.all().count()

    try:
        open_contracts_percentage = (open_contracts/all_contract) * 100
    except:
        open_contracts_percentage = 0

    try:
        active_contracts_percentage = (active_contracts/all_contract) * 100
    except:
        active_contracts_percentage = 0

    all_properties = Properties.objects.filter(
        user=request.user, managed_by_manyumba=False).count()
    try:
        approved_percentage = (approved_properties/all_properties) * 100
    except:
        approved_percentage = 0

    try:
        pending_percentage = (pending_properties/all_properties) * 100
    except:
        pending_percentage = 0

    try:
        active_listings_percentage = (active_listings/all_properties) * 100
    except:
        active_listings_percentage = 0

    try:
        off_market_properties_percentage = (off_market_properties/all_properties) * 100
    except:
        off_market_properties_percentage = 0

    context = {
        'approved_properties': approved_properties,
        'pending_properties': pending_properties,
        'active_listings': active_listings,
        'off_market_properties': off_market_properties,
        'approved_percentage': approved_percentage,
        'pending_percentage': pending_percentage,
        'active_listings_percentage': active_listings_percentage,
        'off_market_properties_percentage': off_market_properties_percentage,


        'open_contracts': open_contracts,
        'open_contracts_percentage': open_contracts_percentage,

        'active_contracts': active_contracts,
        'active_contracts_percentage': active_contracts_percentage,

        
    }

    
    return render(request, 'HouseListing/dashboard_listing.html', context)

def news_letter_subscrptions(request):
    all_subscriptions = EmailSubscribers.objects.all()
    context = {
        'all_subscriptions': all_subscriptions,
    }
    return render(request, 'HouseListing/news_letter_subscrptions.html', context)


def create_listing_listing(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')

    
    else:
        try:
            current_user_status = request.user.userprofile.account_verified

            if current_user_status:

                if request.method == 'GET':
                    form = PropertiesForm(request.POST or None)
                    try:
                        land_id = Type.objects.get(name='Land').id
                    
                    except:
                        land_ = Type.objects.create(
                            name = 'Land'
                        )
                        
                    try:
                        office_id = Type.objects.get(name='Office Space').id
                    
                    except:
                        land_ = Type.objects.create(
                            name = 'Office Space'
                        )

                        office_id = land_.id
                    context = {
                        'form': form,
                        'land_id':land_id,
                        'office_id':office_id,
                        'side': 'listing_side',
                    }
                    return render(request, 'HouseListing/create_listing_listing.html', context)

                else:
                    # get the fields
                    city = request.POST.get('city')
                    prop_city = Cities.objects.get(id=city)

                    street = request.POST.get('street')

                    # page 2
                    property_title = request.POST.get('property_title')
                    description = request.POST.get('description')

                    # get type instance
                    type = request.POST.get('type')
                    prop_type = Type.objects.get(id=type)

                    # get status instance
                    status = request.POST.get('status')
                    prop_status = PropertyStatus.objects.get(id=status)


                    # get landsize instance
                

                    land_id = Type.objects.get(name='Land').id

                    if int(type) == land_id:
                        landsize = request.POST.get('landsize')
                        prop_landsize = LandSizes.objects.get(id=landsize)
                    else:
                        prop_landsize = None
                    
                    area_size = request.POST.get('area_size')

                    price = request.POST.get('price')
                    price = int(price)

                    # deposit = request.POST.get('deposit')
                    # deposit = int(price)

                    # fields for non-land properties
                    rooms = request.POST.get('rooms')
                    bedrooms = request.POST.get('bedrooms')
                    bathrooms = request.POST.get('bathrooms')
                    garages = request.POST.get('garages')

                    publish = request.POST.get('publish')

                    if publish == 'Yes':
                        pre_publish = True
                    else:
                        pre_publish = False

                    # amenities
                    Water = request.POST.get('Water', False)
                    if Water == 'on':
                        Water = True
                    Electricity = request.POST.get('Electricity', False)
                    if Electricity == 'on':
                        Electricity = True
                    Wifi = request.POST.get('WIFI', False)
                    if Wifi == 'on':
                        Wifi = True

                    Ac = request.POST.get('Ac', False)
                    if Ac == 'on':
                        Ac = True
                    Gateman = request.POST.get('Gateman', False)
                    if Gateman == 'on':
                        Gateman = True
                    Parking = request.POST.get('Parking', False)
                    if Parking == 'on':
                        Parking = True
                    Swimming_Pool = request.POST.get('Swimming_Pool', False)
                    if Swimming_Pool == 'on':
                        Swimming_Pool = True
                    Balcony = request.POST.get('Balcony', False)
                    if Balcony == 'on':
                        Balcony = True
                    Gym = request.POST.get('Gym', False)
                    if Gym == 'on':
                        Gym = True
                    Play_Area = request.POST.get('Play_Area', False)
                    if Play_Area == 'on':
                        Play_Area = True

                    # land

                    ElectricSupply = request.POST.get('ElectricSupply', False)
                    if ElectricSupply == 'on':
                        ElectricSupply = True
                    WaterSupply = request.POST.get('WaterSupply', False)
                    if WaterSupply == 'on':
                        WaterSupply = True
                    RainWaterDrainage = request.POST.get('RainWaterDrainage', False)
                    if RainWaterDrainage == 'on':
                        RainWaterDrainage = True
                    DomesticSewage = request.POST.get('DomesticSewage', False)
                    if DomesticSewage == 'on':
                        DomesticSewage = True

                    # bussiness

                    BusinessLounge = request.POST.get('BusinessLounge', False)
                    if BusinessLounge == 'on':
                        BusinessLounge = True    
                    Majortransportlinks = request.POST.get('Majortransportlinks', False)
                    if Majortransportlinks == 'on':
                        Majortransportlinks = True    
                    MeetingRooms = request.POST.get('MeetingRooms', False)
                    if MeetingRooms == 'on':
                        MeetingRooms = True    
                    cctv= request.POST.get('CCTV', False)
                    if cctv== 'on':
                        cctv= True    
                    Elevator= request.POST.get('Elevator', False)
                    if Elevator== 'on':
                        Elevator= True   
                    

                    

                    # media
                    featured_image = request.FILES.get('featured_image')
                    living_room_media = request.FILES.getlist('living_room_media')
                    bedroom_media = request.FILES.getlist('bedroom_media')
                    bathroom_media = request.FILES.getlist('bathroom_media')
                    latitude = request.POST.get('latitude')
                    longitude = request.POST.get('longitude')




                    new_property = Properties.objects.create(
                        user=request.user,
                        property_title=property_title,
                        description=description,
                        type=prop_type,
                        status=prop_status,
                        publish=pre_publish,
                        price=price,
                        # security_deposit=deposit,
                        area_size=area_size,
                        landsize=prop_landsize,
                        rooms=rooms,
                        bedrooms=bedrooms,
                        bathrooms=bathrooms,
                        managed_by_manyumba=False,
                        garages=garages,
                        city=prop_city,
                        street=street,
                        featured_image=featured_image,
                        latitude=latitude,
                        longitude=longitude,
                        # amenities

                        Water=Water,
                        Electricity=Electricity,
                        WFI=Wifi,
                        Ac=Ac,
                        Gateman=Gateman,
                        Parking=Parking,
                        Swimming_Pool=Swimming_Pool,
                        Balcony=Balcony,
                        Gym=Gym,
                        Play_Area=Play_Area,
                        
                        ElectricSupply=ElectricSupply,
                        WaterSupply=WaterSupply,
                        RainWaterDrainage=RainWaterDrainage,
                        DomesticSewage=DomesticSewage,
                        BusinessLounge=BusinessLounge,
                        Majortransportlinks=Majortransportlinks,
                        MeetingRooms=MeetingRooms,
                        CCTV=cctv,
                        Elevator=Elevator,

                    )

                    type_name = new_property.type.name
                    print('==============================')
                    print(type_name)
                    if type_name == 'Land' or type_name == 'Office Space':
                        for media in living_room_media:
                            PropertyImages.objects.create(
                                property=new_property,
                                image=media,
                                home_tag='Other images'
                            )
                    else:
                        for media in living_room_media:
                            PropertyImages.objects.create(
                                property=new_property,
                                image=media,
                                home_tag='living_room'
                            )
                    
                    for media in bedroom_media:
                        PropertyImages.objects.create(
                            property=new_property,
                            image=media,
                            home_tag='bed_room'
                        )
                    
                    for media in bathroom_media:
                        PropertyImages.objects.create(
                            property=new_property,
                            image=media,
                            home_tag='bathroom'
                        )
                    messages.success(request, 'Property created successfully')
                    return redirect('HouseListing:listing_dashboard')
            else:
                messages.warning(request, 'You need to verify your account before you can perfrom this action')
                return redirect('HouseListing:listing_dashboard')
        except:
            # this user doesn't have any userprofile
            return redirect('HouseListing:create_profile', option='listing')


def my_listing(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        active_properties = Properties.objects.filter(user=request.user, managed_by_manyumba=False, approved_by_admin=1, publish=True)
        off_market_properties = Properties.objects.filter(
            Q(user=request.user, managed_by_manyumba=False, approved_by_admin=0, publish=False) | 
            Q(user=request.user, managed_by_manyumba=False, approved_by_admin=True, publish=False)|
            Q(user=request.user, managed_by_manyumba=False, approved_by_admin=0, publish=True) |
            Q(user=request.user, managed_by_manyumba=False, approved_by_admin=2, publish=False) |
            Q(user=request.user, managed_by_manyumba=False, approved_by_admin=2, publish=True)
        )
        context = {
            'active_properties': active_properties,
            'off_market_properties': off_market_properties,
        }
        return render(request, 'HouseListing/my_listings.html', context)


def mylisting_detail(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        this_property = Properties.objects.get(id=pk)
        all_associated_avatars = PropertyImages.objects.filter(
            property=this_property)
        context = {
            'property': this_property,           
            'all_associated_avatars': all_associated_avatars,
        }
        return render(request, 'HouseListing/mylisting_detail.html', context)


def register_subscriber(request):
    print(request.GET)
    email = request.GET.get('email')

    try:
        EmailSubscribers.objects.get(email=email)
    except ObjectDoesNotExist:
        EmailSubscribers.objects.create(
            email = email
        )

    return JsonResponse({'status': 'success'}) # Return a proper HTTP response




def edit_mylisting(request, pk, side):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        if request.method == 'GET':
            this_property = Properties.objects.get(id=pk)
            form = EditListingForm(instance=this_property)
            if side == 'listing':
                apartment_id = ''
            else:
                try:
                    apartment_id = Type.objects.get(name='Apartment').id
                except:
                    apartment_ = Type.objects.create(
                        name = 'Apartment'
                    )

                    apartment_id = apartment_.id
            
            try:
                land_id = Type.objects.get(name='Land').id
            
            except:
                land_ = Type.objects.create(
                    name = 'Land'
                )

                land_id = land_.id
            
            if side == 'listing':
                for_rent = ''
            else:
                try:
                    for_rent = PropertyStatus.objects.get(property_status='For Rent').id
                except:
                    for_rent_ = PropertyStatus.objects.create(
                        property_status = 'For Rent'
                    )
                    for_rent = for_rent_.id

            try:
                office_id = Type.objects.get(name='Office Space').id
            
            except:
                land_ = Type.objects.create(
                    name = 'Office Space'
                )

                office_id = land_.id
                
            if side == 'listing':
                my_template = 'HouseListing/default_listing_base.html'
            else:
                my_template = 'HouseListing/default_base.html'

            context = {
                'form': form,
                'property': this_property,
                'for_rent': for_rent,
                'apartment_id': apartment_id,
                'office_id': office_id,
                'land_id': land_id,
                'my_template': my_template,
                'side': side,
            }
            return render(request, 'HouseListing/mylisting_edit.html', context)
        else:
            this_property = Properties.objects.get(id=pk)
            form = EditListingForm(request.POST, instance=this_property)

            
            if form.is_valid():
                print('we are here')
                obj = form.save(commit=False)
                obj.publish = this_property.publish
                obj.save()
                messages.success(request, 'Update successfull')
                if side == 'listing':
                    return redirect('HouseListing:mylisting_detail', pk=this_property.id)
                else:
                    return redirect('HouseListing:property_details', pk=this_property.id)

            else:
                print(form.errors)
                form = EditListingForm(instance=this_property)
                context = {

                }

            return HttpResponse('error')

def mortgages_leads(request, price, pk):
    context = {
        'price': price,
        'pk': pk,
    }
    return render(request, 'HouseListing/mortgages_leads.html', context)


def create_morgage_lead(request, pk):
    if request.method == 'POST':
        # get fields

        redirect_property = Properties.objects.get(id=pk)
        slug = redirect_property.slug
        full_name = request.POST.get('Name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        employment_type = request.POST.get('employment_type')
        monthly_gross_income = request.POST.get('monthly_gross_income')
        convenient_time_to_be_contacted = request.POST.get('convenient_time_to_be_contacted')
        property_price = request.POST.get('property_price')

        # save
        MorgageLeads.objects.create(
            property = redirect_property,
            full_name=full_name,
            phone=phone,
            email=email,
            employment_type=employment_type,
            gross_income=monthly_gross_income,
            convinient_time=convenient_time_to_be_contacted,
            property_price=property_price
        )
        messages.success(request, 'Application sent successfully. Our team will get back to you in a short while.')
        return redirect('HouseListing:listing_details', slug=slug)
    else:
        messages.warning(request, 'Error 404')
        return redirect('HouseListing:home')


def create_loan_relocation_lead(request):
    if request.method == 'POST':
        full_name = request.POST.get('Name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        current_town = request.POST.get('town')
        employment_type = request.POST.get('employment_type')
        monthly_gross_income = request.POST.get('monthly_gross_income')
        convenient_time_to_be_contacted = request.POST.get(
            'convenient_time_to_be_contacted')
        property_price = request.POST.get('property_price')

        # save
        RelocationLeads.objects.create(
            full_name=full_name,
            phone=phone,
            email=email,
            current_town=current_town,
            employment_type=employment_type,
            gross_income=monthly_gross_income,
            convinient_time=convenient_time_to_be_contacted,
            property_rent=property_price
        )
        messages.success(request, 'Application sent successfully. Our team will get back to you in a short while.')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.warning(request, 'Error 404')
        return redirect('HouseListing:home')


def create_loan_relocation_lead_with_prop(request, pk):
    if request.method == 'POST':

        this_prop = Properties.objects.get(id=pk) 
        slug = this_prop.slug
        full_name = request.POST.get('Name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        current_town = request.POST.get('town')
        employment_type = request.POST.get('employment_type')
        monthly_gross_income = request.POST.get('monthly_gross_income')
        convenient_time_to_be_contacted = request.POST.get(
            'convenient_time_to_be_contacted')
        property_price = request.POST.get('property_price')

        # save
        RelocationLeads.objects.create(
            property = this_prop,
            full_name=full_name,
            phone=phone,
            email=email,
            current_town=current_town,
            employment_type=employment_type,
            gross_income=monthly_gross_income,
            convinient_time=convenient_time_to_be_contacted,
            property_rent=property_price
        )
        messages.success(request, 'Application sent successfully. Our team will get back to you in a short while.')
        return redirect('HouseListing:listing_details', slug=slug)
    else:
        messages.warning(request, 'Error 404')
        return redirect('HouseListing:home')


def mortage_loans(request):
    return render(request, 'HouseListing/mortage_loans.html')


def mortage_loans_details(request):
    return render(request, 'HouseListing/mortage_loans_details.html')


def mortage_relocation(request):
    
    return render(request, 'HouseListing/mortgage_relocation.html')


def create_loan_relocation_lead_detail(request, pk):
    this_prop = Properties.objects.get(id=pk)
    max_loan = int(this_prop.price) * 2
    context = {
        'this_prop':this_prop,
        'max_loan':max_loan,
    }
    
    return render(request, 'HouseListing/mortgage_relocation_with_property_detail.html', context)

def listings_for_sale(request):
    all_listings = Properties.objects.filter(approved_by_admin=1, publish=True, status__property_status='For Sale').order_by('-id')
    count = all_listings.count()
    context = {
        'all_listings': all_listings,
        'listing_status': 'For Sale',
        'form_filter_page': 'listings_for_sale',
        'count': count,
    }

    return render(request, 'HouseListing/shared_listings.html', context)

def listings_abroad(request):
    all_listings = Properties.objects.filter(approved_by_admin=1, publish=True, status__property_status='For Sale').order_by('-id')
    count = all_listings.count()
    context = {
        'all_listings': all_listings,
        'listing_status': 'For Sale',
        'form_filter_page': 'listings_for_sale',
        'count': count,
    }
    return render(request, 'HouseListing/shared_listings.html', context)


def listings_for_rent(request):
    all_listings = Properties.objects.filter(approved_by_admin=1, publish=True, status__property_status='For Rent').order_by('-id')
    count = all_listings.count()
    context = {
        'all_listings': all_listings,
        'listing_status': 'For Rent',
        'form_filter_page': 'listings_for_rent',
        'count': count,
    }

    return render(request, 'HouseListing/shared_listings.html', context)




def search_property_for_sale(request):
    if request.method == 'GET':
        q = request.GET.get('for_sale_location', None)
        if q is None or q == '':
            return redirect('HouseListing:listings_for_sale')
        else:
            all_listings = Properties.objects.filter(
                Q(property_title__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Sale') | 
                Q(type__name__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Sale')|
                Q(city__city_name__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Sale')|
                Q(street__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Sale')
            ).order_by('-id')
            count = all_listings.count()
            result_header = ' for ' + str(q)
            context = {
                'all_listings': all_listings,
                'listing_status': 'For Sale',
                'result_header': result_header,
                'count': count,
                'form_filter_page': 'search_property_for_sale',
            }
            return render(request, 'HouseListing/shared_listings.html', context)

    else:
        messages.warning(request, 'Bad request 404')
        return redirect('HouseListing:home')



def search_property_for_rent(request):
    if request.method == 'GET':
        q = request.GET.get('for_rent_location', None)
        if q is None or q == '':
            return redirect('HouseListing:listings_for_rent')
        else:
            all_listings = Properties.objects.filter(
                Q(property_title__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Rent') | 
                Q(type__name__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Rent')|
                Q(city__city_name__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Rent')|
                Q(street__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Rent')
            ).order_by('-id')
            count = all_listings.count()
            result_header = ' for ' + str(q)
            context = {
                'all_listings': all_listings,
                'listing_status': 'For Rent',
                'result_header': result_header,
                'count': count,
                'form_filter_page': 'search_property_for_rent',
            }
            return render(request, 'HouseListing/shared_listings.html', context)

    else:
        messages.warning(request, 'Bad request 404')
        return redirect('HouseListing:home')


def search_property_for_lease(request):
    if request.method == 'GET':
        q = request.GET.get('for_lease_location', None)
        if q is None or q == '':
            return redirect('HouseListing:home')
        else:
            all_listings = Properties.objects.filter(
                Q(property_title__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Lease') | 
                Q(type__name__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Lease')|
                Q(city__city_name__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Lease')|
                Q(street__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Lease')
            ).order_by('-id')
            count = all_listings.count()
            result_header = ' for ' + str(q)
            context = {
                'all_listings': all_listings,
                'listing_status': 'For Lease',
                'result_header': result_header,
                'form_filter_page': 'search_property_for_lease',
                'count': count,
            }
            return render(request, 'HouseListing/shared_listings.html', context)

    else:
        messages.warning(request, 'Bad request 404')
        return redirect('HouseListing:home')


# the town sliders on home page.
def search_listing_town(request, town):
    
    all_listings = Properties.objects.filter(
        approved_by_admin=1, publish=True,city__city_name=town
    ).order_by('-id')
    count = all_listings.count()
    result_header = ' for ' + str(town)
    context = {
        'all_listings': all_listings,
        'result_header': result_header,
        'count': count,
        'town': town,
    }
    return render(request, 'HouseListing/search_listing_town.html', context)


# menu views
def return_houses_for_sale(request):
    all_listings = Properties.objects.filter(approved_by_admin=1, publish=True, status__property_status='For Sale').exclude(
        approved_by_admin=1, publish=True, status__property_status='For Sale',type__name='Apartment'
    ).exclude(approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Office Space').exclude(approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Land').exclude(approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Warehouse').order_by('-id')
    count = all_listings.count()
    context = {
        'all_listings': all_listings,
        'listing_status': 'For Sale',
        'count': count,
        'form_filter_page': 'return_houses_for_sale',
    }
    return render(request, 'HouseListing/shared_listings.html', context)


def return_houses_for_rent(request):
    all_listings = Properties.objects.filter(approved_by_admin=1, publish=True, status__property_status='For Rent').exclude(
        approved_by_admin=1, publish=True, status__property_status='For Rent',type__name='Apartment'
    ).exclude(approved_by_admin=1, publish=True, status__property_status='For Rent', type__name='Office Space').exclude(approved_by_admin=1, publish=True, status__property_status='For Rent', type__name='Land').exclude(approved_by_admin=1, publish=True, status__property_status='For Rent', type__name='Warehouse').order_by('-id')
    count = all_listings.count()
    context = {
        'all_listings': all_listings,
        'listing_status': 'For Rent',
        'count': count,
        'form_filter_page': 'return_houses_for_rent',
    }
    return render(request, 'HouseListing/shared_listings.html', context)


def return_land_for_sale(request):
    all_listings = Properties.objects.filter(
        approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Land').order_by('-id')
    count = all_listings.count()
    context = {
        'all_listings': all_listings,
        'listing_status': 'For Sale',
        'not_house': 'Land',
        'count': count,
        'form_filter_page': 'return_land_for_sale',
    }
    return render(request, 'HouseListing/shared_listings.html', context)


def return_apartments_for_sale(request):
    all_listings = Properties.objects.filter(
        approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Apartment').order_by('-id')
    count = all_listings.count()
    context = {
        'all_listings': all_listings,
        'listing_status': 'For Sale',
        'not_house': 'Apartments',
        'count': count,
        'form_filter_page': 'return_apartments_for_sale',
    }
    return render(request, 'HouseListing/shared_listings.html', context)


def return_apartments_for_rent(request):
    all_listings = Properties.objects.filter(
        approved_by_admin=1, publish=True, status__property_status='For Rent', type__name='Apartment').order_by('-id')
    count = all_listings.count()
    context = {
        'all_listings': all_listings,
        'listing_status': 'For Rent',
        'not_house': 'Apartments',
        'count': count,
        'form_filter_page': 'return_apartments_for_rent',
    }
    return render(request, 'HouseListing/shared_listings.html', context)



def return_commercial_for_sale(request):
    all_listings = Properties.objects.filter(
        Q(approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Office Space')|
        Q(approved_by_admin=1, publish=True,
          status__property_status='For Sale', type__name='Shops')
        ).order_by('-id')
    count = all_listings.count()
    context = {
        'all_listings': all_listings,
        'listing_status': 'For Sale',
        'not_house': 'Commercial Properties',
        'count': count,
        'form_filter_page': 'return_commercial_for_sale',
    }
    return render(request, 'HouseListing/shared_listings.html', context)


def return_commercial_for_rent(request):
    all_listings = Properties.objects.filter(
        Q(approved_by_admin=1, publish=True, status__property_status='For Rent', type__name='Office Space')|
        Q(approved_by_admin=1, publish=True,
          status__property_status='For Rent', type__name='Shops')
        ).order_by('-id')
    count = all_listings.count()
    context = {
        'all_listings': all_listings,
        'listing_status': 'For Rent',
        'not_house': 'Commercial Properties',
        'count': count,
        'form_filter_page': 'return_commercial_for_rent',
    }
    return render(request, 'HouseListing/shared_listings.html', context)




def filter_return_houses(request, form_filter_page, listing_status):
    # get all fields
    
    print(request.GET)
    price_range = request.GET.get('price_range')

    category = request.GET.get('category')
    category = int(category)

    city = request.GET.get('city')
    city = int(city)
    bathrooms = request.GET.get('bathrooms')
    bedrooms = request.GET.get('bedrooms')

    # price sanitization

    lower_bound = price_range.split('-')[0].strip()
    lower_bound = lower_bound.replace('$', '')
    lower_bound = lower_bound.replace(',', '')

    upper_bound = price_range.split('-')[1].strip()
    upper_bound = upper_bound.replace('$', '')
    upper_bound = upper_bound.replace(',', '')

    # check white query set to use

    if form_filter_page == 'return_houses_for_sale':
        not_house = ''
        all_listings = Properties.objects.filter(approved_by_admin=1, publish=True, status__property_status='For Sale').exclude(
            approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Apartment'
        ).exclude(approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Office Space').exclude(approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Land').exclude(approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Warehouse').order_by('-id')
    elif form_filter_page == 'return_houses_for_rent':
        not_house = ''
        all_listings = Properties.objects.filter(approved_by_admin=1, publish=True, status__property_status='For Rent').exclude(
            approved_by_admin=1, publish=True, status__property_status='For Rent',type__name='Apartment'
        ).exclude(approved_by_admin=1, publish=True, status__property_status='For Rent', type__name='Office Space').exclude(approved_by_admin=1, publish=True, status__property_status='For Rent', type__name='Land').exclude(approved_by_admin=1, publish=True, status__property_status='For Rent', type__name='Warehouse').order_by('-id')
    elif form_filter_page == 'return_land_for_sale':
        not_house = 'Land'
        all_listings = Properties.objects.filter(
            approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Land').order_by('-id')
    elif form_filter_page == 'return_apartments_for_sale':
        not_house = 'Apartment'
        all_listings = Properties.objects.filter(
            approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Apartment').order_by('-id')
    elif form_filter_page == 'return_apartments_for_rent':
        not_house = 'Apartment'
        all_listings = Properties.objects.filter(
            approved_by_admin=1, publish=True, status__property_status='For Rent', type__name='Apartment').order_by('-id')
    elif form_filter_page == 'return_commercial_for_sale':
        not_house = 'Commercial Properties'
        all_listings = Properties.objects.filter(
            Q(approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Office Space')|
            Q(approved_by_admin=1, publish=True,
            status__property_status='For Sale', type__name='Shops')
            ).order_by('-id')
    elif form_filter_page == 'return_commercial_for_rent':
        not_house = 'Commercial Properties'
        all_listings = Properties.objects.filter(
            Q(approved_by_admin=1, publish=True, status__property_status='For Rent', type__name='Office Space')|
            Q(approved_by_admin=1, publish=True,
            status__property_status='For Rent', type__name='Shops')
        ).order_by('-id')

    # For search on pages
    elif form_filter_page == 'search_property_for_sale':

        not_house = ''
        all_listings = Properties.objects.filter(approved_by_admin=1, publish=True).order_by('-id')


    elif form_filter_page == 'search_property_for_rent':

        not_house = ''
        all_listings = Properties.objects.filter(approved_by_admin=1, publish=True).order_by('-id')


    elif form_filter_page == 'search_property_for_lease':

        not_house = ''
        all_listings = Properties.objects.filter(approved_by_admin=1, publish=True).order_by('-id')

    # for sale and rent cards on homepage query

    elif form_filter_page == 'listings_for_sale':

        not_house = ''
        all_listings = Properties.objects.filter(approved_by_admin=1, publish=True, status__property_status='For Sale').order_by('-id')

    elif form_filter_page == 'listings_for_rent':

        not_house = ''
        all_listings = Properties.objects.filter(approved_by_admin=1, publish=True, status__property_status='For Rent').order_by('-id')





    all_listings = all_listings.filter(price__gte=lower_bound, price__lte=upper_bound).order_by('-id')

    if category != 0:
        all_listings = all_listings.filter(type__id = category).order_by('-id')
    if city != 0:
        all_listings = all_listings.filter(city_id = city).order_by('-id')
    if bathrooms != '':
        all_listings = all_listings.filter(bathrooms = bathrooms).order_by('-id')
    if bedrooms != '':
        all_listings = all_listings.filter(bedrooms = bedrooms).order_by('-id')

    count = all_listings.count()



    

    context = {
        'all_listings': all_listings,
        'listing_status': listing_status,
        'not_house': not_house,
        'count': count,
        'form_filter_page': form_filter_page,
        'bathrooms': bathrooms,
        'bedrooms': bedrooms,
        'category': category,
        'city': city,
    }
    return render(request, 'HouseListing/shared_listings.html', context)


def sort_price(request,form_filter_page, listing_status):
    # get fileds
    q_criteria = request.GET.get('q_criteria')

    if q_criteria == '0':
        return redirect(request.META.get('HTTP_REFERER'))
    elif q_criteria == 'l2h':
            if form_filter_page == 'return_houses_for_sale':
                not_house = ''
                all_listings = Properties.objects.filter(approved_by_admin=1, publish=True, status__property_status='For Sale').exclude(
                    approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Apartment'
                ).exclude(approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Office Space').exclude(approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Land').exclude(approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Warehouse').order_by('price')
            elif form_filter_page == 'return_houses_for_rent':
                not_house = ''
                all_listings = Properties.objects.filter(approved_by_admin=1, publish=True, status__property_status='For Rent').exclude(
                    approved_by_admin=1, publish=True, status__property_status='For Rent',type__name='Apartment'
                ).exclude(approved_by_admin=1, publish=True, status__property_status='For Rent', type__name='Office Space').exclude(approved_by_admin=1, publish=True, status__property_status='For Rent', type__name='Land').exclude(approved_by_admin=1, publish=True, status__property_status='For Rent', type__name='Warehouse').order_by('price')
            elif form_filter_page == 'return_land_for_sale':
                not_house = 'Land'
                all_listings = Properties.objects.filter(
                    approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Land').order_by('price')
            elif form_filter_page == 'return_apartments_for_sale':
                not_house = 'Apartment'
                all_listings = Properties.objects.filter(
                    approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Apartment').order_by('price')
            elif form_filter_page == 'return_apartments_for_rent':
                not_house = 'Apartment'
                all_listings = Properties.objects.filter(
                    approved_by_admin=1, publish=True, status__property_status='For Rent', type__name='Apartment').order_by('price')
            elif form_filter_page == 'return_commercial_for_sale':
                all_listings = Properties.objects.filter(
                    Q(approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Office Space')|
                    Q(approved_by_admin=1, publish=True,
                    status__property_status='For Sale', type__name='Shops')
                    ).order_by('price')
            elif form_filter_page == 'return_commercial_for_rent':
                not_house = 'Commercial Properties'
                all_listings = Properties.objects.filter(
                    Q(approved_by_admin=1, publish=True, status__property_status='For Rent', type__name='Office Space')|
                    Q(approved_by_admin=1, publish=True,
                    status__property_status='For Rent', type__name='Shops')
                ).order_by('price')

            # For search on pages
            elif form_filter_page == 'search_property_for_sale':

                not_house = ''
                all_listings = Properties.objects.filter(approved_by_admin=1, publish=True).order_by('price')


            elif form_filter_page == 'search_property_for_rent':

                not_house = ''
                all_listings = Properties.objects.filter(approved_by_admin=1, publish=True).order_by('price')


            elif form_filter_page == 'search_property_for_lease':

                not_house = ''
                all_listings = Properties.objects.filter(approved_by_admin=1, publish=True).order_by('price')

            # for sale and rent cards on homepage query

            elif form_filter_page == 'listings_for_sale':

                not_house = ''
                all_listings = Properties.objects.filter(approved_by_admin=1, publish=True, status__property_status='For Sale').order_by('price')

            elif form_filter_page == 'listings_for_rent':

                not_house = ''
                all_listings = Properties.objects.filter(
                    approved_by_admin=1, publish=True, status__property_status='For Rent').order_by('price')

            count = all_listings.count()
            context = {
                'all_listings': all_listings,
                'listing_status': listing_status,
                'not_house': not_house,
                'count': count,
                'form_filter_page': form_filter_page,
            }
            return render(request, 'HouseListing/shared_listings.html', context)
    elif q_criteria == 'h2l':
            if form_filter_page == 'return_houses_for_sale':
                not_house = ''
                all_listings = Properties.objects.filter(approved_by_admin=1, publish=True, status__property_status='For Sale').exclude(
                    approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Apartment'
                ).exclude(approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Office Space').exclude(approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Land').exclude(approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Warehouse').order_by('-price')
            elif form_filter_page == 'return_houses_for_rent':
                not_house = ''
                all_listings = Properties.objects.filter(approved_by_admin=1, publish=True, status__property_status='For Rent').exclude(
                    approved_by_admin=1, publish=True, status__property_status='For Rent',type__name='Apartment'
                ).exclude(approved_by_admin=1, publish=True, status__property_status='For Rent', type__name='Office Space').exclude(approved_by_admin=1, publish=True, status__property_status='For Rent', type__name='Land').exclude(approved_by_admin=1, publish=True, status__property_status='For Rent', type__name='Warehouse').order_by('-price')
            elif form_filter_page == 'return_land_for_sale':
                not_house = 'Land'
                all_listings = Properties.objects.filter(
                    approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Land').order_by('-price')
            elif form_filter_page == 'return_apartments_for_sale':
                not_house = 'Apartment'
                all_listings = Properties.objects.filter(
                    approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Apartment').order_by('-price')
            elif form_filter_page == 'return_apartments_for_rent':
                not_house = 'Apartment'
                all_listings = Properties.objects.filter(
                    approved_by_admin=1, publish=True, status__property_status='For Rent', type__name='Apartment').order_by('-price')
            elif form_filter_page == 'return_commercial_for_sale':
                all_listings = Properties.objects.filter(
                    Q(approved_by_admin=1, publish=True, status__property_status='For Sale', type__name='Office Space')|
                    Q(approved_by_admin=1, publish=True,
                    status__property_status='For Sale', type__name='Shops')
                    ).order_by('-price')
            elif form_filter_page == 'return_commercial_for_rent':
                not_house = 'Commercial Properties'
                all_listings = Properties.objects.filter(
                    Q(approved_by_admin=1, publish=True, status__property_status='For Rent', type__name='Office Space')|
                    Q(approved_by_admin=1, publish=True,
                    status__property_status='For Rent', type__name='Shops')
                ).order_by('-price')

            # For search on pages
            elif form_filter_page == 'search_property_for_sale':

                not_house = ''
                all_listings = Properties.objects.filter(approved_by_admin=1, publish=True).order_by('-price')


            elif form_filter_page == 'search_property_for_rent':

                not_house = ''
                all_listings = Properties.objects.filter(approved_by_admin=1, publish=True).order_by('-price')


            elif form_filter_page == 'search_property_for_lease':

                not_house = ''
                all_listings = Properties.objects.filter(
                    approved_by_admin=1, publish=True).order_by('-price')

            # for sale and rent cards on homepage query

            elif form_filter_page == 'listings_for_sale':

                not_house = ''
                all_listings = Properties.objects.filter(approved_by_admin=1, publish=True, status__property_status='For Sale').order_by('-price')

            elif form_filter_page == 'listings_for_rent':

                not_house = ''
                all_listings = Properties.objects.filter(
                    approved_by_admin=1, publish=True, status__property_status='For Rent').order_by('-price')

            count = all_listings.count()
            context = {
                'all_listings': all_listings,
                'listing_status': listing_status,
                'not_house': not_house,
                'count': count,
                'form_filter_page': form_filter_page,
            }
            return render(request, 'HouseListing/shared_listings.html', context)
  

def togglePublish(request,pk):
    this_property = Properties.objects.get(id=pk)
    this_property.publish = not this_property.publish
    this_property.save()

    messages.success(request, 'Preference saved')
    return redirect(request.META.get('HTTP_REFERER'))


def listing_profile(request, option):
    # try to get current user profile
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        try:
            UserProfile.objects.get(user=request.user)

            if option == 'listing':
                my_template = 'HouseListing/default_listing_base.html'
                side = 'listing'
            else:
                my_template = 'HouseListing/default_base.html'
                side = 'management'
            

            context = {
                'my_template': my_template,
                'side': side,
            }
            return render(request, 'HouseListing/listing_profile.html', context)
        except:
            messages.info(request, 'Please create your profile')
            return redirect('HouseListing:create_profile', option=option)



def manage_profile(request):
    # try to get current user profile
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        try:
            UserProfile.objects.get(user=request.user)
            return render(request, 'HouseListing/manage_profile.html')
        except:
            messages.info(request, 'Please create your profile')

            return redirect('HouseListing:manage_create_profile')


def listing_delete_property(request, pk):
    target_property = Properties.objects.get(id=pk)
    target_property.delete()
    messages.success(request, 'Property deleted successfully')
    return redirect(request.META.get('HTTP_REFERER'))



# ends here


def approve_listing(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        properties = Properties.objects.filter(approved_by_admin=0)
        context = {
            'properties': properties,
        }
        return render(request, 'HouseListing/approve_properties.html', context)



def admin_morgage_leads(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    
    if request.user.is_superuser:
        leads = MorgageLeads.objects.all()
    else:
        leads = MorgageLeads.objects.filter(property__user = request.user)

    context = {
        'leads': leads,
    }
    return render(request, 'HouseListing/morgage_leads.html', context)
            


def schedule_tour(request, pk):
    if request.method == 'Get':
        messages.warning(request, '404 forbiden.')
        return redirect('HouseListing:home')
    else:
        property = Properties.objects.get(id=pk)
        full_name = request.POST.get('Name')
        phone = request.POST.get('Phone')
        date = request.POST.get('date')
        booking_msg = request.POST.get('booking_msg')

        Tours.objects.create(
            property=property,
            full_name = full_name,
            phone = phone,
            tour_date = date,
            message = booking_msg
        )
        messages.success(request, 'Tour schedule has been received. We will contact you soon with further instructions')
        return redirect(request.META.get('HTTP_REFERER'))


def admin_tours(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')

    if request.user.is_superuser:
        pending_tours = Tours.objects.filter(visited=False, mark_as_span=False)
        history_tours = Tours.objects.filter(
            Q(visited=True, mark_as_span=False)|
            Q(visited=False, mark_as_span=True)|
            Q(visited=True, mark_as_span=True)
        )
    else:

        pending_tours = Tours.objects.filter(visited=False, mark_as_span=False, property__user=request.user)
        history_tours = Tours.objects.filter((
            Q(visited=True, mark_as_span=False)|
            Q(visited=False, mark_as_span=True)|
            Q(visited=True, mark_as_span=True)) &
            Q(property__user=request.user)
        )
        
    context = {
        'pending_tours': pending_tours,
        'history_tours': history_tours,

    }
    return render(request, 'HouseListing/admin_tours.html', context)


def mark_tour_as_complete(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    tour = Tours.objects.get(id=pk)
    tour.visited = True
    tour.save()
    messages.success(request, 'Tour Updated successfully')
    return redirect(request.META.get('HTTP_REFERER'))


def mark_tour_as_spam(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    tour = Tours.objects.get(id=pk)
    tour.mark_as_span = True
    tour.save()
    messages.success(request, 'Tour Marked as spam')
    return redirect(request.META.get('HTTP_REFERER'))


def approve_property_detail(request,pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:    
        this_property = Properties.objects.get(id=pk)
        property_houses = this_property.house_set.all()
        all_associated_avatars = PropertyImages.objects.filter(property=this_property)
        floor_plans = FloorPlans.objects.filter(property=this_property)

        #cases

        all_cases = LegalCase.objects.filter(property=this_property)
        context = {
            'property': this_property,
            'property_houses': property_houses,
            'all_associated_avatars': all_associated_avatars,
            'floor_plans': floor_plans,
            'is_approve': True,
            'all_cases': all_cases,

        }
        return render(request, 'HouseListing/approve_property_detail.html', context)


def property_details(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        this_property = Properties.objects.get(id=pk)
        property_houses = this_property.house_set.all()
        all_associated_avatars = PropertyImages.objects.filter(property=this_property)
        active_tenants = Lease.objects.filter(
            apartment__id=pk, current_status=True).count()
        floor_plans = FloorPlans.objects.filter(property=this_property)
        all_cases = LegalCase.objects.filter(property=this_property)
        all_contractors = MaintenanceContract.objects.filter(property=this_property)



        # financials


        payments = Payment.objects.filter(invoice__lease__apartment=this_property).annotate(
            month=TruncMonth('date_paid')
        ).values('month').annotate(total_amount=Sum('amount_paid')).order_by('-month')


        # current month aggregates

        # Get the current month
        now = datetime.datetime.now()
        current_month_start = timezone.make_aware(timezone.datetime(now.year, now.month, 1))
        current_month_end = timezone.make_aware(timezone.datetime(now.year, now.month + 1, 1)) if now.month < 12 else timezone.make_aware(timezone.datetime(now.year + 1, 1, 1))
         # Aggregate payments for the current month
        current_month_payments = Payment.objects.filter(
            invoice__lease__apartment=this_property,
            date_paid__gte=current_month_start,
            date_paid__lt=current_month_end
        ).aggregate(total_amount=Sum('amount_paid'))['total_amount'] or 0
    



        context = {
            'property': this_property,
            'property_houses': property_houses,
            'all_associated_avatars': all_associated_avatars,
            'floor_plans': floor_plans,
            'active_tenants': active_tenants,
            'all_cases': all_cases,
            'all_contractors': all_contractors,
            'payments': payments,
            'current_month_payments': current_month_payments,
            'now': now
        }
        return render(request, 'HouseListing/approve_property_detail.html', context)


def approve_property(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:    
        this_property = Properties.objects.get(id=pk)
        this_property.approved_by_admin = 1
        this_property.save()

        # send email
        message = 'This is to inform you that your property' + this_property.property_title + 'has been Approved and is now live'
        send_mail('April Management Property Status',
          message,
          'info@aprilmanagement.pro',
          [
            this_property.user.email, # add more emails to this list of you want to
          ]
        )

        messages.success(request, 'Property Approved successfully')
        return redirect('HouseListing:approve_listing')


def reject_property(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:    
        this_property = Properties.objects.get(id=pk)
        this_property.approved_by_admin = 2
        this_property.save()

        message = 'This is to inform you that your property' + this_property.property_title + 'has been REJECTED.'
        send_mail('April Management Property Status',
          message,
          'info@aprilmanagement.pro',
          [
            this_property.user.email, # add more emails to this list of you want to
          ]
        )
        messages.success(request, 'Property Rejected')
        return redirect('HouseListing:approve_listing')


def home(request):
    # If user is authenticated, redirect them to their appropriate dashboard
    if request.user.is_authenticated:
        try:
            if request.user.userprofile.user_account_type == 'Tenant':
                return redirect('HouseListing:tenant_dashboard')
            else:
                return redirect('HouseListing:dashboard')
        except:
            # If there's an issue with user profile, redirect to main dashboard
            return redirect('HouseListing:dashboard')
    else:
        # If user is not authenticated, redirect to the new Portfolio landing page
        return redirect('info')

def old_home(request):
    all_listings = Properties.objects.filter(approved_by_admin=1, publish=True).order_by('-id')
    all_cities = Cities.objects.all()


    context = {
        'all_listings':all_listings,
        'all_cities':all_cities,
    }
    return render(request, 'HouseListing/home-listing.html', context)


def listing_details(request, slug):

    property = Properties.objects.get(slug=slug)
    try:
        featured_image = PropertyImages.objects.get(property=property, featured=True)
    except ObjectDoesNotExist:
        featured_image = ''
    print('featured image above')
    print(featured_image)

    try:
        images = PropertyImages.objects.filter(property=property)
    except:
        images = ''

    # rental criteria
    try:
        rental_criteria = RentalCriteria.objects.get(property=property)
    except:
        rental_criteria = ''
    
    context = {
        'property': property,
        'featured_image': featured_image,
        'images': images,
        'rental_criteria': rental_criteria,
    }
    return render(request, 'HouseListing/listing-details.html', context)

def coming_soon(request):
    return render(request, 'HouseListing/coming_soon.html')

def tenant_dashboard(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    
    else:
        tenant = Tenant.objects.get(t_user=request.user)
        active_lease = Lease.objects.filter(tenant__id=tenant.id, current_status=True)
        # calc rent balance

        all_leases = Lease.objects.filter(tenant__t_user=request.user).order_by('-id')
        total_rent_balance = 0

        excess_payment = 0
       
        
        for lease in all_leases:
            invoices = InvoiceHybrid.objects.filter(lease=lease).order_by('-month')
            pending_invoices = invoices.filter(payment_status='Pending')
            rent_balance = sum(invoice.balance for invoice in pending_invoices)
            total_rent_balance += rent_balance
        
            try:
                last_invoice = invoices.first()                
                

                # check if balance is less than 0 
                if last_invoice.balance < 0:
                    excess_payment += abs(last_invoice.balance)
           
            except:
                print('no invoice')
                pass
        print(excess_payment)

        context = {
            'tenant': tenant,
            'active_lease': active_lease,
            'total_rent_balance': total_rent_balance,
            'excess_payment': excess_payment,
        }
        return render(request, 'HouseListing/tenant_dashboard.html', context)


def vacation_notice(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        if request.method == 'GET':
            messages.warning(request, '404 forbidden.')
            return redirect('HouseListing:tenant_dashboard')
        else:
            # get fields
            vacate_date = request.POST.get('vacate_date')
            units = request.POST.getlist('units')
            remarks = request.POST.get('remarks', None)

            for unit in units:
                unit = int(unit)
                lease_instance = Lease.objects.get(id=unit)
                VacateNotice.objects.create(
                    lease = lease_instance,
                    vacate_date = vacate_date,
                    remarks = remarks
                )
            messages.success(request, 'Vacate Notice send successfully. The Landlord will get back to you soon!')
            return redirect(request.META.get('HTTP_REFERER'))


def vacate_notice_list(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        active_vacation_notices = VacateNotice.objects.filter(lease__apartment__user = request.user, vacated=False)
        previous_vacation_notices = VacateNotice.objects.filter(lease__apartment__user = request.user, vacated=True)

        context = {
            'active_vacation_notices': active_vacation_notices,
            'previous_vacation_notices': previous_vacation_notices,
        }
        return render(request, 'HouseListing/vacate_notice_list.html', context)


def tenant_properties(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        all_leases = Lease.objects.filter(tenant__t_user=request.user).order_by('-id')


        for lease in all_leases:
            invoices = InvoiceHybrid.objects.filter(lease=lease).order_by('-month')
            pending_invoices = invoices.filter(payment_status='Pending')

            rent_balance = sum(invoice.balance for invoice in pending_invoices)
            lease.rent_balance = rent_balance


        context = {
            'all_leases': all_leases,
            'title': 'List Of All Units Associated To You'
        }
        return render(request, 'HouseListing/tenant_associated_leases.html', context)


def tenant_property_details(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        try:
            lease = Lease.objects.get(id=pk)
        except:
            messages.warning(request, 'Sorry property with such Id does not exist')
            return redirect('HouseListing:tenant_properties')

        
        invoices = InvoiceHybrid.objects.filter(lease=lease).order_by('-month')

        pending_invoices = invoices.filter(payment_status='Pending')
        paid_invoices = invoices.filter(payment_status='Paid')

        # compute rent balance for this lease
        rent_balance = 0
        for invoice in pending_invoices:
            rent_balance += invoice.balance

        print(rent_balance)
        # get excess payment
        # get last invoice
        excess_payment = 0.00
        try:
            last_invoice = invoices.first()
            print(last_invoice.balance)
            

            # check if balance is less than 0 
            if last_invoice.balance < 0:
                excess_payment = abs(last_invoice.balance)
        except:
            pass

            
        all_payments = Payment.objects.filter(invoice__lease=lease)

        

        context = {
            'lease': lease,
            'pending_invoices': pending_invoices,
            'paid_invoices': paid_invoices,
            'rent_balance': rent_balance,
            'excess_payment': excess_payment,
            'all_payments': all_payments,
        }
        return render(request, 'HouseListing/tenant_associated_lease_details.html', context)


def tenant_invoices(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        all_invoices = InvoiceHybrid.objects.filter(lease__tenant__t_user = request.user).order_by('-month')

        show_clear = False
        # first check if params query current_month = 1
        if request.GET.get('current_month') == '1':
            current_date = datetime.datetime.now()
            all_invoices = all_invoices.filter(month__year=current_date.year, month__month=current_date.month)
            show_clear = True

        # we have to seperate them to pending and paid
        pending_invoices = all_invoices.filter(payment_status='Pending')
        paid_invoices = all_invoices.filter(payment_status='Paid')


        context = {    
            'pending_invoices': pending_invoices,
            'paid_invoices': paid_invoices,
            'show_clear': show_clear,
            'is_in_management': False
        }
        return render(request, 'HouseListing/tenant_invoices.html', context)

def pay_rent_list(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        if request.method == 'GET':
            all_leases = Lease.objects.filter(tenant__t_user=request.user).order_by('-id')

            for lease in all_leases:
                invoices = InvoiceHybrid.objects.filter(lease=lease).order_by('-month')
                pending_invoices = invoices.filter(payment_status='Pending')

                rent_balance = sum(invoice.balance for invoice in pending_invoices)
                lease.rent_balance = rent_balance


            context = {
                'all_leases': all_leases,
                'title': 'Select Unit To Pay Rent.',
            }

            return render(request, 'HouseListing/pay_rent_list.html', context)
        else:
            pass


# 3eV9SX6a53T4avh9
# 8gXk29R8

# signature key 

"""

537C7E98D4CB0C65729964E4A73C9D5710830A76DF431C0AFFF6B7EAA4AE4123E277F9619A333C917F693BC898D0A40D8484E025DA343A7D50FAA703E5823BEF

webhook https://aprilmanagement.pro/webhook_payments
"""
def get_an_accept_payment_page(amount, lease_id):
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = "7xf25cUCJW98"
    merchantAuth.transactionKey = "3dJ7UdG25Z87mPT3"

    setting1 = apicontractsv1.settingType()
    setting1.settingName = apicontractsv1.settingNameEnum.hostedPaymentButtonOptions
    setting1.settingValue = "{\"text\": \"Pay\"}"

    setting2 = apicontractsv1.settingType()
    setting2.settingName = apicontractsv1.settingNameEnum.hostedPaymentOrderOptions
    setting2.settingValue = "{\"show\": false}"

    setting3 = apicontractsv1.settingType()
    setting3.settingName = apicontractsv1.settingNameEnum.hostedPaymentReturnOptions
    continue_url = f"https://aprilmanagement.pro/pay_rent/{lease_id}/{amount}/"
    setting3.settingValue = f"""{{
        "showReceipt": true,
        "url": "{continue_url}",
        "urlText": "Continue",
        "cancelUrl": "https://aprilmanagement.pro/tenant_properties",
        "cancelUrlText": "Cancel"
    }}"""

    settings = apicontractsv1.ArrayOfSetting()
    settings.setting.append(setting1)
    settings.setting.append(setting2)
    settings.setting.append(setting3)

    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType = "authCaptureTransaction"
    transactionrequest.amount = amount

    paymentPageRequest = apicontractsv1.getHostedPaymentPageRequest()
    paymentPageRequest.merchantAuthentication = merchantAuth
    paymentPageRequest.transactionRequest = transactionrequest
    paymentPageRequest.hostedPaymentSettings = settings

    paymentPageController = getHostedPaymentPageController(paymentPageRequest)

    paymentPageController.execute()

    paymentPageResponse = paymentPageController.getresponse()

    if paymentPageResponse is not None:
        if paymentPageResponse.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
            print('Successfully got hosted payment page!')

            

            return {'success': True, 'token': str(paymentPageResponse.token)}

            # if paymentPageResponse.messages is not None:
            #     print('Message Code : %s' % paymentPageResponse.messages.message[0]['code'].text)
            #     print('Message Text : %s' % paymentPageResponse.messages.message[0]['text'].text)
        else:

            if paymentPageResponse.messages is not None:
                print('Failed to get batch statistics.\nCode:%s \nText:%s' % (paymentPageResponse.messages.message[0]['code'].text,paymentPageResponse.messages.message[0]['text'].text))

            error_code = paymentPageResponse.messages.message[0]['code'].text
            error_text = paymentPageResponse.messages.message[0]['text'].text
            return {'success': False, 'error_code': error_code, 'error_text': error_text}           

    return {'success': False, 'error_code': 'Unknown', 'error_text': 'No response from payment gateway'}


# get_an_accept_payment_page(100)


@csrf_exempt
def payment_token_view(request, pk):
    if request.method == 'POST':
        amount = request.POST.get('amount_paid', '10.00')  # Default amount to 10.00 if not specified
        response = get_an_accept_payment_page(amount, pk)

        print(response['token'])
        if response['success']:
            return JsonResponse({'token': response['token'], 'status': 'success'}, status=200)
        else:
            return JsonResponse({'error': response['error_text'], 'status': 'error'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)



def pay_rent_form(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        if request.method == 'GET':
            lease = Lease.objects.get(id=pk)
            invoices = InvoiceHybrid.objects.filter(lease=lease).order_by('-month')
            pending_invoices = invoices.filter(payment_status='Pending')

            rent_balance = 0
            for invoice in pending_invoices:
                rent_balance += invoice.balance



            
            context = {
                'lease': lease,
                'rent_balance': rent_balance,
            }

            return render(request, 'HouseListing/pay_rent_form.html', context)
        else:



            lease = Lease.objects.get(id=pk)
            amount_paid = request.POST.get('amount_paid')




            pay_rent(request, pk, amount_paid)

            messages.success(request, 'Rent payment successful')
            return redirect('HouseListing:tenant_properties')


def tenant_request_repair(request, r_type):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    
    if request.method == 'GET':
        all_leases = Lease.objects.filter(tenant__t_user=request.user).order_by('-id')
        if r_type == 'request':
            past_requests = RepairRequest.objects.filter(lease__tenant__t_user=request.user).order_by('-id')
        else:
            past_requests = Complain.objects.filter(lease__tenant__t_user=request.user).order_by('-id')

        context = {
            'all_leases': all_leases,
            'past_requests': past_requests,
            'r_type': r_type,
        }
        return render(request, 'HouseListing/tenant_request_repair.html', context)


def tenant_request_repair_details(request, pk, r_type):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    
    if request.method == 'GET':
        lease = Lease.objects.get(id=pk)
        context = {
            'lease': lease,
            'r_type': r_type,
        }
        
        return render(request, 'HouseListing/tenant_request_repair_details.html', context)
    else:
        pass
        
    

def submit_repair_request(request, lease_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')

    if request.method == 'POST':
        user = request.user


        lease = Lease.objects.get(id=lease_id)
        priority = request.POST.get('priority')
        description = request.POST.get('description')
        repair_deadline = request.POST.get('repair_deadline')

        # we have everything now

        RepairRequest.objects.create(
            lease = lease,
            request_priority = priority,
            request_details = description,
            request_deadline = repair_deadline
        )

        messages.success(request, 'Repair request submitted successfully')
        return redirect(request.META.get('HTTP_REFERER'))
        


def submit_tenant_complain(request, lease_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')

    if request.method == 'POST':
        user = request.user

        lease = Lease.objects.get(id=lease_id)
        description = request.POST.get('description')

        # we have everything now

        Complain.objects.create(
            lease = lease,
            complain_details = description,
        )

        messages.success(request, 'Complain submitted successfully')
        return redirect(request.META.get('HTTP_REFERER'))




def landloard_repair_list(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    
    if request.user.is_superuser:
        # pending and completed
        pending_requests = RepairRequest.objects.filter(request_completed=False)
        completed_requests = RepairRequest.objects.filter(request_completed=True)
        
    else:
        pending_requests = RepairRequest.objects.filter(lease__apartment__user=request.user, request_completed=False).order_by('-id')
        completed_requests = RepairRequest.objects.filter(lease__apartment__user=request.user, request_completed=True).order_by('-id')

    context = {
        'pending_requests': pending_requests,
        'completed_requests': completed_requests,
    }
    return render(request, 'HouseListing/landloard_repair_list.html', context)


def landloard_tenant_complaints(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    
    if request.user.is_superuser:
        # pending and completed
        pending_complaints = Complain.objects.filter(complain_resolved=False)
        completed_complaints = Complain.objects.filter(complain_resolved=True)
        
    else:
        pending_complaints = Complain.objects.filter(lease__apartment__user=request.user, complain_resolved=False).order_by('-id')
        completed_complaints = Complain.objects.filter(lease__apartment__user=request.user, complain_resolved=True).order_by('-id')

    context = {
        'pending_complaints': pending_complaints,
        'completed_complaints': completed_complaints,
    }
    return render(request, 'HouseListing/landloard_complaint_list.html', context)
    

def resolve_complaint(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    
    complain = Complain.objects.get(id=pk)
    complain.complain_resolved = True
    # update the status of the complain
    complain.complain_status = 'Resolved'

    # update resolution date - its a datefield
    complain.resolution_date = datetime.datetime.now()
    complain.save()

    messages.success(request, 'Complaint resolved successfully')
    return redirect(request.META.get('HTTP_REFERER'))

def invoice_template(request, pk):
    invoice = InvoiceHybrid.objects.get(id=pk)
    generation_date = invoice.month
    gmonth = generation_date.month

    invoice_lease_id = invoice.lease.id
    invoice_count = Invoice.objects.filter(lease_id=invoice_lease_id).count()
    if invoice_count > 1:
        over_due = invoice.lease.running_balance - invoice.amount_incurred
    else:
        over_due = 0

    # get all past invoices that have a balnce > 0
    past_invoices = InvoiceHybrid.objects.filter(lease_id=invoice_lease_id, balance__gt=0, month__lt=invoice.month).order_by('-month')


    # get subtotal
    subtotal = 0
    for past_invoice in past_invoices:
        subtotal += past_invoice.balance

    # add current month rent
    subtotal += invoice.balance

    amount_paid = invoice.current_amount - invoice.balance
    
    

    context = {
        'invoice': invoice,
        'gmonth': gmonth,
        'over_due': over_due,
        'ipk': 'my_lease_pk',
        'past_invoices': past_invoices,
        'subtotal': subtotal,
        'amount_paid': amount_paid,
    }
    return render(request, 'HouseListing/invoice_template.html', context)


def generate_monthly_invoices(request):
    # current_month = datetime.datetime.now().date().replace(day=1)  # First day of the current month
    current_month = '2024-05-01'

    active_leases = Lease.objects.filter(current_status=True)  # Active leases

    for lease in active_leases:
        # Calculate the total overdue amount from all unpaid invoices
        # Calculate the current month's rent (assuming rent is stored in lease.house.rent)
        current_amount = lease.house.rent
        balance_to_set = lease.house.rent
        


        unpaid_invoices = lease.invoices_hybrid.filter(
            Q(month__lt=datetime.datetime.now().date().replace(day=1)) &
            Q(payment_status='Pending') | 
            Q(payment_status='Partial') 
        )

        print(unpaid_invoices)

        # get previous month invoice
        previous_month_invoice = lease.invoices_hybrid.filter(month__lt=current_month).order_by('-month').first()
        overflow_amout = 0
        # check to see if balance is less than 0
        if previous_month_invoice is not None:
            if previous_month_invoice.balance < 0:
                overflow_amout = previous_month_invoice.balance
                balance_to_set += previous_month_invoice.balance
                previous_month_invoice.balance = 0
                previous_month_invoice.save()
       

        # Create a new invoice for the current month

        payment_status = 'Pending' if balance_to_set > 0 else 'Paid'
        new_invoice = InvoiceHybrid.objects.create(
            lease=lease,
            balance = balance_to_set,
            current_amount=current_amount,
            payment_status= payment_status,
            month=current_month,
            billing_for='Rent'
        )

        if overflow_amout != 0:
            # create payment for current invoice
            # overflow is negative, change it positive
            overflow_amout = abs(overflow_amout)
            Payment.objects.create(invoice=new_invoice, amount_paid=overflow_amout,payment_method='Overpayment')
            
            




    return HttpResponse('Invoices generated successfully')


def pay_rent(request, lease_id, amount_paid):
    # try:
        lease = Lease.objects.get(id=lease_id)
        amount_paid = Decimal(amount_paid)



        with transaction.atomic():  # Ensure database integrity during the update process
            remaining_amount = amount_paid


            invoices = lease.invoices_hybrid.filter(payment_status__in=['Pending', 'Partial'])
            property_inst = lease.apartment



            if len(invoices) == 0:
                # take latests invoice and inflate balance so that it's negative
                latest_invoice = lease.invoices_hybrid.order_by('-month').first()
                # check if balance is negative
                latest_invoice.balance = latest_invoice.balance - remaining_amount
                latest_invoice.save()


            else:
                while remaining_amount > 0:
                    # Get the oldest invoice
                    
                    oldest_invoice = lease.invoices_hybrid.filter(payment_status__in=['Pending', 'Partial']).order_by('month').first()

                    # check oldest_invoice has value
                    if oldest_invoice is None:
                        break

                    if len(lease.invoices_hybrid.filter(payment_status__in=['Pending', 'Partial']).order_by('month')) > 1:
                        if oldest_invoice.balance <= remaining_amount:
                            Payment.objects.create(invoice=oldest_invoice, amount_paid=oldest_invoice.balance)
                            oldest_invoice.payment_status = 'Paid'
                            remaining_amount -= oldest_invoice.balance
                            oldest_invoice.balance = 0
                            # save the invoice
                            oldest_invoice.save()
                        else:
                            # Partial payment of the invoice
                            Payment.objects.create(invoice=oldest_invoice, amount_paid=remaining_amount)
                            oldest_invoice.payment_status = 'Pending'
                            oldest_invoice.balance -= remaining_amount
                            oldest_invoice.save()
                            remaining_amount = 0
                        
                    elif len(lease.invoices_hybrid.filter(payment_status__in=['Pending', 'Partial']).order_by('month')) == 1:
                        Payment.objects.create(invoice=oldest_invoice, amount_paid=remaining_amount)

                        # oldest_invoice.payment_status = 'Pending'
                        # update status depending on the amount paid
                        if oldest_invoice.balance == remaining_amount:
                            oldest_invoice.payment_status = 'Paid'
                            oldest_invoice.balance = 0
                            remaining_amount = 0
                        elif oldest_invoice.balance < remaining_amount:
                            oldest_invoice.payment_status = 'Paid'
                            oldest_invoice.balance -= remaining_amount
                            remaining_amount -= 0
                        elif oldest_invoice.balance > remaining_amount:
                            oldest_invoice.payment_status = 'Pending'
                            oldest_invoice.balance -= remaining_amount
                            remaining_amount = 0

                        oldest_invoice.save()

            property_inst.balance += float(amount_paid)
            property_inst.save()


        messages.success(request, 'Payment successful')
        return redirect('HouseListing:tenant_properties')
    # except Lease.DoesNotExist:
    #     return render(request, 'payments/error.html', {'message': 'Lease not found.'})
    # except Exception as e:
    #     return render(request, 'payments/error.html', {'message': f'An error occurred: {str(e)}'})

def dashboard(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        all_properties_count = Properties.objects.filter(
            user=request.user, managed_by_manyumba=True).count()
        approved_properties = Properties.objects.filter(
            user=request.user, managed_by_manyumba=True, approved_by_admin=1).count()
        pending_properties = Properties.objects.filter(user=request.user,managed_by_manyumba=True, approved_by_admin=0).count()
        active_listings = Properties.objects.filter(user=request.user,managed_by_manyumba=True, approved_by_admin=1, publish=True).count()
        off_market_properties = Properties.objects.filter(
            Q(user=request.user, managed_by_manyumba=True, approved_by_admin=0, publish=False) | Q(
                user=request.user, managed_by_manyumba=True, approved_by_admin=1, publish=False) | Q(user=request.user, managed_by_manyumba=True, approved_by_admin=0, publish=True)
        ).count()

        all_properties = Properties.objects.filter(
            user=request.user, managed_by_manyumba=True).count()
        all_properties_obj = Properties.objects.filter(
            user=request.user, managed_by_manyumba=True)


          # Get the current month
        now = datetime.datetime.now()
        current_month_start = timezone.make_aware(timezone.datetime(now.year, now.month, 1))
        current_month_end = timezone.make_aware(timezone.datetime(now.year, now.month + 1, 1)) if now.month < 12 else timezone.make_aware(timezone.datetime(now.year + 1, 1, 1))
         # Aggregate payments for the current month
        current_month_payments = Payment.objects.filter(
            invoice__lease__apartment__user= request.user,
            date_paid__gte=current_month_start,
            date_paid__lt=current_month_end
        ).aggregate(total_amount=Sum('amount_paid'))['total_amount'] or 0


        # summation of all account balances
        account_balance = 0
        for property_ in all_properties_obj:
            account_balance += property_.balance

        # compute total billed
        total_billed = 0
        # get all_invoices associated to properties owned by this user
        all_invoices = InvoiceHybrid.objects.filter(lease__apartment__user=request.user)

        for invoice in all_invoices:
            total_billed += invoice.current_amount

        
        




        
        
        

        

        vacant_units = House.objects.filter(apartment__user=request.user, vacant=True).count()
        all_houses = House.objects.filter(apartment__user=request.user).count()

        if all_houses == 0:
            occupancy_percentage = 0
        else:
            occupancy_percentage = ((all_houses - vacant_units) / all_houses) * 100

        all_tenants = Tenant.objects.filter(user=request.user).count()

        try:
            approved_percentage = (approved_properties/all_properties) * 100
        except:
            approved_percentage = 0

        try:
            pending_percentage = (pending_properties/all_properties) * 100
        except:
            pending_percentage = 0

        try:
            active_listings_percentage = (active_listings/all_properties) * 100
        except:
            active_listings_percentage = 0

        try:
            off_market_properties_percentage = (off_market_properties/all_properties) * 100
        except:
            off_market_properties_percentage = 0

        context = {
            'vacant_units': vacant_units,
            'all_houses': all_houses,
            'all_tenants': all_tenants,
            'approved_properties': approved_properties,
            'pending_properties': pending_properties,
            'active_listings': active_listings,
            'off_market_properties': off_market_properties,
            'approved_percentage': approved_percentage,
            'pending_percentage': pending_percentage,
            'active_listings_percentage': active_listings_percentage,
            'off_market_properties_percentage': off_market_properties_percentage,

            'all_properties_count': all_properties_count,
            'occupancy_percentage': occupancy_percentage,
            'now': now,
            'current_month_payments': current_month_payments,
            'account_balance': account_balance,
            'total_billed': total_billed,
            
        }

        return render(request, 'HouseListing/dashboard.html', context)


def properties(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
       
        properties = Properties.objects.filter(user=request.user,managed_by_manyumba=True).order_by('-id')
        context = {
            'properties': properties,
        }
        return render(request, 'HouseListing/property_list.html', context)


def admin_listed_properties(request):
    if not request.user.is_authenticated and not request.user.is_superuser:
        messages.warning(request, 'Session 404. Contact admin.')
        return redirect('HouseListing:home')
    else:

        properties = Properties.objects.filter(managed_by_manyumba=False)
        context = {
            'properties': properties,
            # 'listed_number': 1,
        }
        return render(request, 'HouseListing/properties.html', context)


def admin_managed_properties(request):
    if not request.user.is_authenticated and not request.user.is_superuser:
        messages.warning(request, 'Session 404. Contact admin.')
        return redirect('HouseListing:home')
    else:

        properties = Properties.objects.filter(managed_by_manyumba=True, publish=False)
        context = {
            'properties': properties,
        }
        return render(request, 'HouseListing/properties.html', context)


def admin_listed_managed_properties(request):
    if not request.user.is_authenticated and not request.user.is_superuser:
        messages.warning(request, 'Session 404. Contact admin.')
        return redirect('HouseListing:home')
    else:

        properties = Properties.objects.filter(managed_by_manyumba=True,publish=True)
        context = {
            'properties': properties,
        }
        return render(request, 'HouseListing/properties.html', context)


def admin_relocation_leads(request):
    if not request.user.is_authenticated and not request.user.is_superuser:
        messages.warning(request, 'Session 404. Contact admin.')
        return redirect('HouseListing:home')
    
    if request.user.is_superuser:
        relocation_leads = RelocationLeads.objects.all().order_by('creation_date')
    else:
        relocation_leads = RelocationLeads.objects.filter(property__user=request.user).order_by('creation_date')

    context = {
        'relocation_leads': relocation_leads,
    }
    return render(request, 'HouseListing/relocation_leads.html', context)


def relocation_lead_complete(request, pk):
    if not request.user.is_authenticated and not request.user.is_superuser:
        messages.warning(request, 'Session 404. Contact admin.')
        return redirect('HouseListing:home')
    else:
        relocation_lead = RelocationLeads.objects.get(id=pk)
        relocation_lead.completed = True
        relocation_lead.save()
        messages.success(request, 'Lead status updated successfully')
        return redirect('HouseListing:admin_relocation_leads')

@transaction.atomic
def create_listing(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        try:
            current_user_status = request.user.userprofile.account_verified

            if current_user_status:
                if request.method == 'GET':
                    try:
                        apartment_id = Type.objects.get(name='Apartment').id
                    except:
                        apartment_ = Type.objects.create(
                            name = 'Apartment'
                        )

                        apartment_id = apartment_.id
                    
                    try:
                        land_id = Type.objects.get(name='Land').id
                    
                    except:
                        land_ = Type.objects.create(
                            name = 'Land'
                        )

                        land_id = land_.id

                    try:
                        for_rent = PropertyStatus.objects.get(property_status='For Rent').id
                    except:
                        for_rent_ = PropertyStatus.objects.create(
                            property_status = 'For Rent'
                        )
                        for_rent = for_rent_.id

                    try:
                        office_id = Type.objects.get(name='Office Space').id
                    
                    except:
                        land_ = Type.objects.create(
                            name = 'Office Space'
                        )

                        office_id = land_.id

                    form = ManagePropertiesForm(request.POST or None)
                    context = {
                        'form': form,
                        'for_rent': for_rent,
                        'apartment_id': apartment_id,
                        'office_id': office_id,
                        'land_id': land_id,
                        'side': 'management_side'
                    }
                    return render(request, 'HouseListing/create-listing.html', context)
                else:
                    # get the fields
                    # try:
                        if request.user.userprofile.user_account_type == 'Demo':
                            messages.success(request, 'Demo registration successfull. Note that this is a demo hence no data was saved.')
                            return redirect('HouseListing:properties')

                        property_title = request.POST.get('property_title')
                        description = request.POST.get('description')

                        type = request.POST.get('type')
                        prop_type = Type.objects.get(id=type)

                        status = request.POST.get('status')
                        prop_status = PropertyStatus.objects.get(id=status)

                        publish = request.POST.get('publish')

                        if publish == 'Yes':
                            pre_publish = True
                        else:
                            pre_publish = False
                        
                        price = request.POST.get('price', 0)
                        price = int(price)


                        area_size = request.POST.get('area_size')

                        land_id = Type.objects.get(name='Land').id
                        if int(type) == land_id and request.POST.get('landsize') != '':
                            landsize = request.POST.get('landsize')
                            prop_landsize = LandSizes.objects.get(id=landsize)
                        else:
                            prop_landsize = None
                        rooms = request.POST.get('rooms')
                        bedrooms = request.POST.get('bedrooms')
                        bathrooms = request.POST.get('bathrooms')
                        garages = request.POST.get('garages')

                        city = request.POST.get('city')
                        prop_city = Cities.objects.get(id=city)

                        street = request.POST.get('street')
                        
                        # amenities

                        Water = request.POST.get('Water', False)
                        if Water == 'on':
                            Water = True
                        Electricity = request.POST.get('Electricity', False)
                        if Electricity == 'on':
                            Electricity = True
                        Wifi = request.POST.get('WIFI', False)
                        if Wifi == 'on':
                            Wifi = True

                        Ac = request.POST.get('Ac', False)
                        if Ac == 'on':
                            Ac = True
                        Gateman = request.POST.get('Gateman', False)
                        if Gateman == 'on':
                            Gateman = True
                        Parking = request.POST.get('Parking', False)
                        if Parking == 'on':
                            Parking = True
                        Swimming_Pool = request.POST.get('Swimming_Pool', False)
                        if Swimming_Pool == 'on':
                            Swimming_Pool = True
                        Balcony = request.POST.get('Balcony', False)
                        if Balcony == 'on':
                            Balcony = True
                        Gym = request.POST.get('Gym', False)
                        if Gym == 'on':
                            Gym = True
                        Play_Area = request.POST.get('Play_Area', False)
                        if Play_Area == 'on':
                            Play_Area = True
                        ElectricSupply = request.POST.get('ElectricSupply', False)
                        if ElectricSupply == 'on':
                            ElectricSupply = True
                        WaterSupply = request.POST.get('WaterSupply', False)
                        if WaterSupply == 'on':
                            WaterSupply = True
                        RainWaterDrainage = request.POST.get('RainWaterDrainage', False)
                        if RainWaterDrainage == 'on':
                            RainWaterDrainage = True
                        DomesticSewage = request.POST.get('DomesticSewage', False)
                        if DomesticSewage == 'on':
                            DomesticSewage = True    
                        BusinessLounge = request.POST.get('BusinessLounge', False)
                        if BusinessLounge == 'on':
                            BusinessLounge = True    
                        Majortransportlinks = request.POST.get('Majortransportlinks', False)
                        if Majortransportlinks == 'on':
                            Majortransportlinks = True    
                        MeetingRooms = request.POST.get('MeetingRooms', False)
                        if MeetingRooms == 'on':
                            MeetingRooms = True    
                        cctv= request.POST.get('CCTV', False)
                        if cctv== 'on':
                            cctv= True    
                        Elevator= request.POST.get('Elevator', False)
                        if Elevator== 'on':
                            Elevator= True   

                        virtual_tour = request.POST.get('virtual_tour', None) 

                        # survey fields
                        minimum_income = request.POST.get('minimum_income', None)
                        credit_score = request.POST.get('credit_score', None)
                        employment_status = request.POST.get('employment_status', None)
                        smoking_allowed_value = request.POST.get('smoking_allowed', None)
                        smoking_allowed = True if smoking_allowed_value == 'Yes' else False

                        pets_allowed_value = request.POST.get('pets_allowed', None)
                        pets_allowed = True if pets_allowed_value == 'Yes' else False

                        max_occupants = request.POST.get('max_occupants', None)


                        # contracts
                        contracts = []

                        contract_indices = {key.split('_')[-1] for key in request.POST.keys() if key.startswith('contract_')}

                        for idx in contract_indices:
                            # Extracting each field for the current meeting
                            c_service_type = request.POST.get(f'contract_service_type_{idx}', '')  # Changed variable name to avoid conflict
                            c_description = request.POST.get(f'contract_description_{idx}', '')  # Changed variable name
                        
                            # Assuming there might be more fields, add them as needed

                            # Append this meeting's data as a dictionary to the meetings list
                            contracts.append({
                                'service_type': c_service_type,  # Use m_title to avoid conflict with event title
                                'description': c_description,  # Use m_description to avoid conflict
                            })

                        


                        # media
                        featured_image = request.FILES.get('featured_image')
                        living_room_media = request.FILES.getlist('living_room_media')
                        bedroom_media = request.FILES.getlist('bedroom_media')
                        bathroom_media = request.FILES.getlist('bathroom_media')

                        inspection_reports = request.FILES.get('inspection_report', None)
                        legal_documents = request.FILES.get('legal_documents', None)





                        # logic
                        auto_house_id = request.POST.get('auto_house_id', False)
                        is_managedbymanyumba = True
                        
                        single_units = request.POST.get('single')
                        bed_sitter = request.POST.get('bed_sitters')
                        one_bedroom = request.POST.get('One_Bedroom')
                        Two_Bedroom = request.POST.get('Two_Bedroom')
                        Three_Bedroom = request.POST.get('Three_Bedroom')

                        latitude = request.POST.get('latitude')
                        longitude = request.POST.get('longitude')   

                        single_rent = request.POST.get('single_rent')
                        bed_sitters_rent = request.POST.get('bed_sitters_rent')
                        one_bedroom_rent = request.POST.get('One_Bedroom_rent')
                        Two_Bedroom_rent = request.POST.get('Two_Bedroom_rent')
                        Three_Bedroom_rent = request.POST.get('Three_Bedroom_rent')

                        total_units = int(single_units) + \
                                        int(bed_sitter) + int(one_bedroom) + int(Two_Bedroom) + int(Three_Bedroom)
                                        
                        default_house_type = ''

                        apartment_id = Type.objects.get(name='Apartment').id

                        if type == apartment_id:
                            if int(single_units) > 0 and int(bed_sitter) == 0 and int(one_bedroom) == 0:
                                default_house_type = 'Single'
                            elif int(single_units) > 0 and int(bed_sitter) > 0 and int(one_bedroom) == 0:
                                default_house_type = 'Single, Bed-Sitter'
                            elif int(single_units) > 0 and int(bed_sitter) > 0 and int(one_bedroom) > 0:
                                default_house_type = 'Single, Bed-Sitter, One-Bedroom'

                        else:
                            default_house_type = 'None'

                                        
                        # now save to the db.
                        new_property = Properties.objects.create(
                            user = request.user,
                            property_title=property_title,
                            description = description,
                            units=int(total_units),
                            available_rooms=int(total_units),
                            default_house_type=default_house_type,
                            type=prop_type,
                            status=prop_status,
                            price = price,
                            area_size = area_size,
                            landsize=prop_landsize,
                            rooms = rooms,
                            bedrooms = bedrooms,
                            bathrooms = bathrooms,
                            garages = garages,
                            managed_by_manyumba = True,
                            publish=pre_publish,
                            city = prop_city,
                            street = street,
                            featured_image = featured_image,  
                            latitude=latitude,
                            longitude=longitude,

                                # amenities

                            Water=Water,
                            Electricity=Electricity,
                            WFI=Wifi,
                            Ac=Ac,
                            Gateman=Gateman,
                            Parking=Parking,
                            Swimming_Pool=Swimming_Pool,
                            Balcony=Balcony,
                            Gym=Gym,
                            Play_Area=Play_Area,
                            
                            ElectricSupply=ElectricSupply,
                            WaterSupply=WaterSupply,
                            RainWaterDrainage=RainWaterDrainage,
                            DomesticSewage=DomesticSewage,
                            BusinessLounge=BusinessLounge,
                            Majortransportlinks=Majortransportlinks,
                            MeetingRooms=MeetingRooms,
                            CCTV=cctv,
                            Elevator=Elevator,   
                            inspection_reports=inspection_reports,
                            legal_documents=legal_documents,
                            virtual_tour_link=virtual_tour,    
                            approved_by_admin =  1       
                        )
                            
                            # create the houses
                        print('we are displaying ids')
                        print(type)
                        print(apartment_id)
                        if int(type) == apartment_id:
                            print('this is a rental aparment')
                            single_loops = int(single_units)
                            bed_sitter_loops = int(bed_sitter)
                            one_bedroom_loops = int(one_bedroom)
                            two_bedroom_loops = int(Two_Bedroom)
                            three_bedromm_loops = int(Three_Bedroom)

                            apartment_loop = Properties.objects.get(pk=new_property.id)

                            # single_loop
                            if auto_house_id:
                                for i in range(1, single_loops + 1):
                                    House.objects.create(
                                        apartment=apartment_loop,
                                        house_code=i,
                                        rent=single_rent,
                                        deposit=single_rent,
                                        house_type='Single',
                                    )
                            else:
                                for i in range(1, single_loops + 1):
                                    House.objects.create(
                                        apartment=apartment_loop,
                                        rent=single_rent,
                                        deposit=single_rent,
                                        house_type='Single',
                                    )
                            if auto_house_id:
                                for i in range(single_loops + 1, single_loops + 1 + bed_sitter_loops):
                                    House.objects.create(
                                        apartment=apartment_loop,
                                        house_code=i,
                                        rent=bed_sitters_rent,
                                        deposit=bed_sitters_rent,
                                        house_type='Bed-Sitter',
                                    )

                            else:
                                for i in range(0, bed_sitter_loops):
                                    House.objects.create(
                                        apartment=apartment_loop,
                                        rent=bed_sitters_rent,
                                        deposit=bed_sitters_rent,
                                        house_type='Bed-Sitter',
                                    )
                            if auto_house_id:
                                for i in range(single_loops + 1 + bed_sitter_loops,
                                            single_loops + 1 + bed_sitter_loops + one_bedroom_loops):
                                    House.objects.create(
                                        apartment=apartment_loop,
                                        house_code=i,
                                        rent=one_bedroom_rent,
                                        deposit=one_bedroom_rent,
                                        house_type='One Bedroom',
                                    )
                            else:
                                for i in range(0, one_bedroom_loops):
                                    House.objects.create(
                                        apartment=apartment_loop,
                                        rent=one_bedroom_rent,
                                        deposit=one_bedroom_rent,
                                        house_type='One Bedroom',
                                    )
                            if auto_house_id:
                                for i in range(single_loops + 1 + bed_sitter_loops + one_bedroom_loops,
                                            single_loops + 1 + bed_sitter_loops + one_bedroom_loops + two_bedroom_loops):
                                    House.objects.create(
                                        apartment=apartment_loop,
                                        house_code=i,
                                        rent=Two_Bedroom_rent,
                                        deposit=Two_Bedroom_rent,
                                        house_type='Two Bedroom',
                                    )
                            else:
                                for i in range(0, two_bedroom_loops):
                                    House.objects.create(
                                        apartment=apartment_loop,
                                        rent=Two_Bedroom_rent,
                                        deposit=Two_Bedroom_rent,
                                        house_type='Two Bedroom',
                                    )
                            if auto_house_id:
                                for i in range(single_loops + 1 + bed_sitter_loops + one_bedroom_loops + two_bedroom_loops,
                                            single_loops + 1 + bed_sitter_loops + one_bedroom_loops + two_bedroom_loops + three_bedromm_loops):
                                    House.objects.create(
                                        apartment=apartment_loop,
                                        house_code=i,
                                        rent=Three_Bedroom_rent,
                                        deposit=Three_Bedroom_rent,
                                        house_type='Three Bedroom',
                                    )
                            else:
                                for i in range(0, two_bedroom_loops):
                                    House.objects.create(
                                        apartment=apartment_loop,
                                        rent=Three_Bedroom_rent,
                                        deposit=Three_Bedroom_rent,
                                        house_type='Three Bedroom',
                                    )
                        else:
                            apartment_loop = Properties.objects.get(pk=new_property.id)
                            type_name = Type.objects.get(id=type).name
                            House.objects.create(
                                apartment=apartment_loop,
                                house_code=1,
                                rent=price,
                                deposit=price,
                                house_type=type_name
                            )
                            apartment_loop.units = 1
                            apartment_loop.available_rooms = 1
                            apartment_loop.save()

                        # save images for the property
                        type_name = new_property.type.name
                        print('==============================')
                        print(type_name)
                        if type_name == 'Land' or type_name == 'Office Space':
                            for media in living_room_media:
                                PropertyImages.objects.create(
                                    property=new_property,
                                    image=media,
                                    home_tag='Other images'
                                )
                        else:
                            for media in living_room_media:
                                PropertyImages.objects.create(
                                    property=new_property,
                                    image=media,
                                    home_tag='living_room'
                                )

                        
                        for media in bedroom_media:
                            PropertyImages.objects.create(
                                property=new_property,
                                image=media,
                                home_tag='bed_room'
                            )
                        
                        for media in bathroom_media:
                            PropertyImages.objects.create(
                                property=new_property,
                                image=media,
                                home_tag='bathroom'
                            )

                        # create survey now
                            
                        RentalCriteria.objects.create(
                            property=new_property,
                            minimum_income=minimum_income,
                            credit_score=credit_score,
                            employment_status=employment_status,
                            smoking_allowed=smoking_allowed,
                            pets_allowed=pets_allowed,
                            max_occupants=max_occupants
                        )

                        # contracts

                        for contract in contracts:
                            MaintenanceContract.objects.create(
                                property = new_property,
                                service_type = contract['service_type'],
                                description = contract['description'],
                            )

                            

                        # save successfully
                            
                        
                        
                        messages.success(request, 'Property created successfully')
                        return redirect('HouseListing:properties')
                    # except:
                    #     messages.warning(request, 'There was a problem creating your Listing. Try again')
                        
                    #     return redirect('HouseListing:properties')
            else:
                messages.warning(request, 'You need to verify your account before you can perfrom this action')
                return redirect('HouseListing:dashboard')
        except Exception as e:
            print(e)
            # this user doesn't have any userprofile
            return redirect('HouseListing:create_profile', option='manage')


def house_details(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:    
        house = House.objects.get(id=pk)
        active_lease = Lease.objects.filter(house_id=pk, current_status=True)
        terminated_leases = Lease.objects.filter(house_id=pk, current_status=False)
        context = {
            'house': house,
            'active_leases': active_lease,
            'terminated_leases': terminated_leases,
        }
        return render(request, 'HouseListing/house_details.html', context)


def update_house(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:    
        t_house = House.objects.get(id=pk)

        if request.method == 'POST':
            house_code = request.POST.get('house_code')
            rent = request.POST.get('rent')

            parent_apartment = t_house.apartment
            property_houses = parent_apartment.house_set.all()

            for house in property_houses:
                if house.house_code == house_code:
                    t_house.rent = rent
                    t_house.save()
                    messages.success(request, 'Rent updated successfully.')
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    t_house.house_code = house_code
                    t_house.rent = rent
                    t_house.save()
                    messages.success(request, 'House details updated successfully.')
                    return redirect(request.META.get('HTTP_REFERER'))
            print(property_houses)



def register_tenant(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        try:
            current_user_status = request.user.userprofile.account_verified

            if current_user_status:
                if request.method == 'GET':
                    form = TenantRegistrationForm(request.POST or None)
                    context = {
                        'form': form
                    }
                    return render(request, 'HouseListing/register_tenant.html', context)
                if request.method == 'POST':
                    if request.user.is_authenticated:
                        form = TenantRegistrationForm(request.POST or None)
                        first_name = form.data['first_name']
                        last_name = form.data['last_name']
                        phone = form.data['phone']
                        gender = form.data['gender']
                        id_number = form.data['id_number']
                        email = form.data['email']

                        Tenant.objects.create(
                            user = request.user,
                            first_name=first_name,
                            last_name=last_name,
                            id_number=id_number,
                            gender=gender,
                            email=email,
                            contact=phone
                        )
                        messages.success(request, 'Tenant created successfully')
                        return redirect('HouseListing:dashboard')
                    else:
                        messages.warning(request, 'You have to be logged in to perform this action')
                        return redirect('HouseListing:dashboard')
        
            else:
                messages.warning(
                    request, 'You need to verify your account before you can perfrom this action')
                return redirect('HouseListing:dashboard')
        except:
            return redirect('HouseListing:create_profile', option='manage')


def tenants_list(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:   
        # try:
        #     current_user_status = request.user.userprofile.account_verified

        #     if current_user_status: 
        properties = Properties.objects.filter(user=request.user, managed_by_manyumba=True,approved_by_admin=1 )
        context = {
            'properties': properties,
        }
        return render(request, 'HouseListing/tenants_list.html', context)
        #     else:
        #         messages.warning(request, 'You need to verify your account before you can perfrom this action')
        #         return redirect('HouseListing:dashboard')
        # except:
        #     # this user doesn't have any userprofile
        #     return redirect('HouseListing:create_profile', option='manage')


def tenant_sub_list(request, pk):
    all_active_tenants = Lease.objects.filter(apartment__id=pk, current_status=True)

    all_terminated_tenants = Lease.objects.distinct().filter(apartment__id=pk, current_status=False)
    # all_terminated_tenants = Lease.objects.filter(apartment__id=pk, current_status=False)


    print(all_terminated_tenants)
    
    this_property = Properties.objects.get(id=pk)

    context = {
        'all_active_tenants': all_active_tenants,
        'all_terminated_tenants': all_terminated_tenants,
        'this_property': this_property,
    }
    return render(request, 'HouseListing/tenant_sub_list.html', context)


def tenant_details(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:    
        tenant = Tenant.objects.get(id=pk)
        all_leases = Lease.objects.filter(tenant=pk)
        all_invoices = InvoiceHybrid.objects.filter(lease__tenant=pk)

        # active house
        active_lease = Lease.objects.filter(tenant__id=pk, current_status=True)

        context = {
            'tenant': tenant,
            'all_leases': all_leases,
            'all_invoices': all_invoices,
            'active_lease': active_lease,
        }
        return render(request, 'HouseListing/tenant_details.html', context)

def edit_tenant(request, pk):
    if request.method == 'GET':
        return redirect('HouseListing:dashboard')
    if request.method == 'POST':
        if request.user.is_authenticated:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')
            gender = request.POST.get('gender')
            id_number = request.POST.get('id_number')
            email = request.POST.get('email')

            tenant_object = Tenant.objects.get(id=pk)
            tenant_object.first_name=first_name
            tenant_object.last_name=last_name
            tenant_object.id_number=id_number
            tenant_object.gender=gender
            tenant_object.email=email
            tenant_object.contact=phone

            tenant_object.save()
            
            messages.success(request, 'Profile Updated successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(
                request, 'You have to be logged in to perform this action')
            return redirect('HouseListing:dashboard')


def property_categories(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        if request.method == 'GET':
            categories = PropertyStatus.objects.all()
            context = {
                'categories': categories
            }
            return render(request, 'HouseListing/property_categories.html', context)
        else:
            property_status = request.POST.get('property_status')
            description = request.POST.get('description')

            PropertyStatus.objects.create(
                property_status=property_status,
                description = description,
            )
            messages.success(request, 'Configuration Saved Successfully')
            return redirect('HouseListing:property_categories')


def delete_property_category(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:    
        category = PropertyStatus.objects.get(id=pk)
        category.delete()
        messages.success(request, 'Configuration Deleted Successfully')
        return redirect('HouseListing:property_categories')


def edit_property_categories(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:    
        category = PropertyStatus.objects.get(id=pk)
        property_status = request.POST.get('property_status')
        description = request.POST.get('description')

        category.property_status = property_status
        category.description = description
        category.save()
        messages.success(request, 'Configuration Updated Successfully')
        return redirect('HouseListing:property_categories')


def property_type(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        if request.method == 'GET':
            property_types = Type.objects.all()
            context = {
                'property_types': property_types
            }
            return render(request, 'HouseListing/property_type.html', context)
        else:
            name = request.POST.get('name')
            name = name.capitalize()

            Type.objects.create(
                name=name,
            )
            messages.success(request, 'Configuration Saved Successfully')
            return redirect('HouseListing:property_type')


def delete_property_type(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:    
        type = Type.objects.get(id=pk)
        type.delete()
        messages.success(request, 'Configuration Deleted Successfully')
        return redirect('HouseListing:property_type')


def edit_property_edit(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        type = Type.objects.get(id=pk)
        
        name = request.POST.get('name')

        type.name = name
        type.save()
        messages.success(request, 'Configuration Updated Successfully')
        return redirect('HouseListing:property_type')


def property_cities(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        if request.method == 'GET':
            cities = Cities.objects.all()
            context = {
                'cities': cities
            }
            return render(request, 'HouseListing/property_cities.html', context)
        else:
            city_name = request.POST.get('city_name').capitalize()

            Cities.objects.create(
                city_name=city_name,
            )
            messages.success(request, 'Configuration Saved Successfully')
            return redirect('HouseListing:property_cities')


def delete_property_city(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        city = Cities.objects.get(id=pk)
        city.delete()
        messages.success(request, 'City Deleted Successfully')
        return redirect('HouseListing:property_cities')


def edit_property_city(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        mycity = Cities.objects.get(id=pk)

        city = request.POST.get('city')

        mycity.city_name = city
        mycity.save()
        messages.success(request, 'City Updated Successfully')
        return redirect('HouseListing:property_cities')


def land_sizes(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        if request.method == 'GET':
            land_sizes = LandSizes.objects.all()
            context = {
                'land_sizes': land_sizes
            }
            return render(request, 'HouseListing/land_sizes.html', context)
        else:
            land_size = request.POST.get('land_size')

            LandSizes.objects.create(
                size=land_size,
            )
            messages.success(request, 'Configuration Saved Successfully')
            return redirect('HouseListing:land_sizes')


def edit_land_sizes(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        land_ = LandSizes.objects.get(id=pk)
        
        land_size = request.POST.get('land_size')

        land_.size = land_size
        land_.save()
        messages.success(request, 'Configuration Updated Successfully')
        return redirect('HouseListing:land_sizes')


def delete_land_size(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        land_ = LandSizes.objects.get(id=pk)
        land_.delete()
        messages.success(request, 'Land Deleted Successfully')
        return redirect('HouseListing:land_sizes')



def register_lease(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        # try:
            current_user_status = request.user.userprofile.account_verified

            if current_user_status:
                if request.method == "GET":
                    form = LeaseForm(request.POST or None, request=request)
                    context = {
                        'form': form,
                    }
                    return render(request, 'HouseListing/register_lease.html', context)
                if request.method == 'POST':
                    form = LeaseForm(request.POST or None,
                                     request.FILES or None, request=request)
                    if form.is_valid():
                        lease = form.save(commit=False)
                        house = lease.house.id

                        lease.lease_documents = request.FILES['lease_documents']

                        house_object = House.objects.get(id=house)
                        if house_object.vacant == False:
                            messages.info(request, 'An error occured but we tried to fix it. Check to see if the lease was successfull if not, Please try again.')
                            return redirect('HouseListing:dashboard')

                        selected_house = House.objects.get(id=house)
                        print(selected_house)
                        selected_house.vacant = False

                        lease.apartment.available_rooms -= 1

                        lease.apartment.save()
                        selected_house.save()
                        
                        rent = house_object.rent
                        lease.running_balance = rent

                        lease.save()
                        lease_object = Lease.objects.get(id=lease.id)

                        ## this is the tenant associated
                        tenant_object = lease_object.tenant

                        ## generate first invoice.
                        apartment = lease.apartment
                        amount_incurred = lease.house.rent
                        date_generated = datetime.date.today()

                        Invoice.objects.create(
                            # apartment=apartment,
                            # house=selected_house,
                            # tenant=tenant_object,
                            lease=lease_object,
                            amount_incurred=amount_incurred,
                            amount_due=amount_incurred,
                            date_generated=date_generated,
                            previous_over_dues=0,
                        )

                        
                        ## create user account for this tenant if they don't have an account.
                        tenants_email = tenant_object.email
                        first_name = tenant_object.first_name
                        full_name = tenant_object.first_name + ' ' + tenant_object.last_name
                        phone_number = tenant_object.contact

                        flag = False  
                        account_exists = False  
                        account_is_tenant = False

                        ## check to see of there is an account with this email.
                        for each_user in User.objects.all():
                            if each_user.email == tenants_email:
                                account_exists = True
                                ## check to see the account_type
                                print('we are in step 1')
                                try:
                                    print('we are inside')
                                    instance_profile = each_user.userprofile

                                    if instance_profile.user_account_type == 'Tenant':
                                        ## he has a tenant account so just activate is
                                        account_is_tenant = True
                                        break
                                    else:
                                        ## the account found is not a tenant account.
                                        flag = True
                                        continue
                                except:
                                    print('we dont have a profile')
                                    flag = True
                                    break   
                            else:
                                print('no email')
                                pass                             

                        if flag or not account_exists:
                            if not account_is_tenant:                            
                               
                                username = phone_number
                                # for each_user in User.objects.all():
                                #     if each_user.username == username:
                                #         username = uuid.uuid4().hex[:30]
                                #         break

                                password = User.objects.make_random_password()

                                user = User.objects.create(
                                    username = username,
                                    email=tenants_email
                                )
                                user.set_password(password)                            
                                user.save()

                                tenant_object.t_user = user
                                tenant_object.save()

                                # create profile
                                UserProfile.objects.create(
                                    user = user,
                                    user_account_type = 'Tenant',
                                    full_name = full_name,
                                    phone_number = phone_number,
                                    email = tenants_email,
                                    account_verified = True
                                )      
                                # send email 
                                mail_subject = 'April Management - Tenant Account.'
                                message = get_template("HouseListing/acc_create_email.html").render({
                                        'first_name': first_name,
                                        'username': username,
                                        'password': password,
                                        'apartment': apartment.property_title,
                                        'house_code': house_object.house_code,
                                    })

                                to_email = tenants_email
                                from_email = 'info@aprilmanagement.pro'
                                
                                email = EmailMessage(
                                    mail_subject, message,from_email, to=[to_email]
                                )
                                email.content_subtype = "html"
                                email.send()
                                messages.success(request, 'Lease created successfully.')
                                return redirect('HouseListing:dashboard')
                            else:
                                mail_subject = 'April Management - Tenant Account.'
                                message = get_template("HouseListing/acc_create_email.html").render({
                                    'first_name': first_name,
                                    'apartment': apartment.property_title,
                                    'house_code': house_object.house_code,
                                })

                                to_email = tenants_email
                                from_email = 'info@aprilmanagement.pro'

                                email = EmailMessage(
                                    mail_subject, message, from_email, to=[to_email]
                                )
                                email.content_subtype = "html"
                                email.send()
                                messages.success(request, 'Lease created successfully.')
                                return redirect('HouseListing:dashboard')
                        else:
                            mail_subject = 'April Management - Tenant Account.'
                            message = get_template("HouseListing/acc_create_email.html").render({
                                    'first_name': first_name,
                                    'apartment': apartment.property_title,
                                    'house_code': house_object.house_code,
                                })

                            to_email = tenants_email
                            from_email = 'info@aprilmanagement.pro'
                            
                            email = EmailMessage(
                                mail_subject, message,from_email, to=[to_email]
                            )
                            email.content_subtype = "html"
                            email.send()
                            messages.success(request, 'Lease created successfully.')
                            return redirect('HouseListing:dashboard')

                    else:
                        print(request.POST)
                        print(form.errors)
                        messages.warning(request, 'The form is invalid. Please retry.')
                        return redirect('HouseListing:dashboard')
            else:
                messages.warning(request, 'You need to verify your account before you can perfrom this action')
                return redirect('HouseListing:dashboard')
        # except:
        #     # this user doesn't have any userprofile
        #     messages.warning(request, 'Sorry an error occured. Contact administrator.')
        #     return redirect('HouseListing:dashboard')

def create_user(request):

    username = uuid.uuid4().hex[:30]

    for each_user in User.objects.all():
        if each_user.username == username:
            username = uuid.uuid4().hex[:30]
            break

    password = User.objects.make_random_password()
    email = 'pta@gmail.com'

    user = User.objects.create(
        username = username
    )
    user.set_password(password)
    user.save()
    return HttpResponse(password)



def tenant_change_password(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')

    if request.method == 'GET':
        return render(request, 'HouseListing/tenant_change_password.html')
    
    if request.method == 'POST':
        new_password = request.POST.get('password')
        user = User.objects.get(username=request.user.username)
        user.set_password(new_password)
        user.save()

        logout(request)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, 'Your password was reset successfully')
        return redirect(request.META.get('HTTP_REFERER'))


def load_houses(request):
    apartment_id = request.GET.get('apartment')
    houses = House.objects.filter(apartment_id=apartment_id, vacant=True)
    context = {
        'houses': houses,
    }
    return render(request, 'HouseListing/house_dropdown.html', context)



def load_tenants(request):
    tenants = Tenant.objects.filter(user=request.user)
    context = {
        'tenants': tenants,
    }
    return render(request, 'HouseListing/tenants_dropdown.html', context)



def lease_list(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        all_active_leases = Lease.objects.filter(apartment__user=request.user, current_status=True)
        all_terminated_leases = Lease.objects.filter(apartment__user=request.user, current_status=False)

        context = {
            'all_active_leases': all_active_leases,
            'all_terminated_leases': all_terminated_leases,
        }

        return render(request, 'HouseListing/lease_list.html', context)


def lease_details(request,pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        try:
            lease = Lease.objects.get(id=pk)
        except:
            messages.warning(request, 'Sorry property with such Id does not exist')
            return redirect('HouseListing:tenant_properties')

        
        invoices = InvoiceHybrid.objects.filter(lease=lease).order_by('-month')

        pending_invoices = invoices.filter(payment_status='Pending')
        paid_invoices = invoices.filter(payment_status='Paid')

        # compute rent balance for this lease
        rent_balance = 0
        for invoice in pending_invoices:
            rent_balance += invoice.balance

        print(rent_balance)
        # get excess payment
        # get last invoice
        excess_payment = 0.00
        try:
            last_invoice = invoices.first()
            print(last_invoice.balance)
            

            # check if balance is less than 0 
            if last_invoice.balance < 0:
                excess_payment = abs(last_invoice.balance)
        except:
            pass

            
        all_payments = Payment.objects.filter(invoice__lease=lease)

        

        context = {
            'lease': lease,
            'pending_invoices': pending_invoices,
            'paid_invoices': paid_invoices,
            'rent_balance': rent_balance,
            'excess_payment': excess_payment,
            'all_payments': all_payments,
        }
        return render(request, 'HouseListing/tenant_associated_lease_details.html', context)

def management_invoices(request):
    all_invoices = InvoiceHybrid.objects.filter(lease__apartment__user = request.user).order_by('-month')

    show_clear = False
    # first check if params query current_month = 1
    if request.GET.get('current_month') == '1':
        current_date = datetime.datetime.now()
        all_invoices = all_invoices.filter(month__year=current_date.year, month__month=current_date.month)
        show_clear = True

    # we have to seperate them to pending and paid
    pending_invoices = all_invoices.filter(payment_status='Pending')
    paid_invoices = all_invoices.filter(payment_status='Paid')

    context = {
        
        'pending_invoices': pending_invoices,
        'paid_invoices': paid_invoices,
        'show_clear': show_clear,
        'is_in_management': True,

    }
    return render(request, 'HouseListing/tenant_invoices.html', context)


def manage_payments(request):
    all_payments = Payment.objects.filter(invoice__lease__apartment__user=request.user).order_by('-date_paid')

    show_clear = False
    # first check if params query current_month = 1
    if request.GET.get('current_month') == '1':
        current_date = datetime.datetime.now()
        all_payments = all_payments.filter(date_paid__year=current_date.year, date_paid__month=current_date.month)
        show_clear = True
    
    context = {
        'all_payments': all_payments,
        'is_in_management': True,
        'show_clear': show_clear,
    }
    return render(request, 'HouseListing/payments.html', context)
    


def terminate_lease(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        house = House.objects.get(id=pk)
        lease = Lease.objects.filter(house_id=pk, current_status=True).first()
        all_notices = VacateNotice.objects.filter(lease=lease, vacated = False)
        tenant = lease.tenant
        if lease:
            lease.current_status = False
            lease.save()

            house.vacant = True
            lease.apartment.available_rooms += 1
            lease.apartment.save()
            house.save()

            if len(all_notices) > 0:
                for each_notice in all_notices:
                    each_notice.vacated = True
                    each_notice.save()

            messages.success(
                request, 'The Lease has been terminated successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, 'unit has no associated lease.')
            return redirect(request.META.get('HTTP_REFERER'))




# invoices
# def invoice_list(request, pk):
#     all_invoices = Invoice.objects.filter(lease=pk).order_by('-date_generated')
#     all_payments = PaidRent.objects.filter(
#         lease=pk).order_by('-payment_for', '-date_paid')

#     context = {
#         'all_invoices': all_invoices,
#         'my_lease_pk': pk,
#         'all_payments': all_payments,
#     }

#     return render(request, 'Tenants/Invoice_list.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next = request.POST.get('next', None)

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['is_demo_tenant'] = False
                messages.success(
                    request, 'Logged in Successfully as ' + request.user.username)
                
                if next is not None and next == 'list':
                    return redirect('HouseListing:listing_dashboard')
                elif next is not None and next == 'manage':
                    return redirect('HouseListing:dashboard')
                elif next is not None and next == 'sale_home':
                    return redirect('HouseListing:create_listing_listing')
                else:
                    try:
                        if user.userprofile.user_account_type == 'Tenant':
                            return redirect('HouseListing:tenant_dashboard')
                        else:
                            return redirect('HouseListing:home')
                    except:
                        return redirect('HouseListing:home')


            else:
                messages.warning(request, 'Account not activated')
                return redirect('HouseListing:home')
        else:
            messages.warning(request, 'Invalid Username or Password!')
            return redirect('HouseListing:home')
    return redirect('HouseListing:home')


def login_demo(request):
    username = 'demo@aprilmanagement.com'
    password = 'AprilRocks'

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            request.session['is_demo_tenant'] = False
            return redirect('HouseListing:dashboard')
    else:
        messages.warning(request, 'sorry an error occurred. Try again later.')
        return redirect('HouseListing:home')


def login_contractor(request):
    username = 'demo@aprilmanagement.com'
    password = 'AprilRocks'

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            request.session['is_demo_tenant'] = False
            return redirect('HouseListing:contractor_my_contracts')
    else:
        messages.warning(request, 'sorry an error occurred. Try again later.')
        return redirect('HouseListing:home')


def login_tenant_demo(request):
    username = 'demo@aprilmanagement.com'
    password = 'AprilRocks'

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            request.session['is_demo_tenant'] = True
            print(request.session.get('is_demo_tenant'))
            return redirect('HouseListing:tenant_dashboard')
    else:
        messages.warning(request, 'sorry an error occurred. Try again later.')
        return redirect('HouseListing:home')


def logout_user(request):
    logout(request)
    try:
        request.session['is_demo_tenant'] = False
    except:
        pass
    messages.success(request, 'Successfully Logged out.')
    return redirect('HouseListing:home')

def demo_logout(request):
    logout(request)
    # messages.success(request, '')
    return redirect('HouseListing:freetrial')

def generate_customer_number():
    # Generate a unique customer number
    time_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    unique_id = str(uuid.uuid4())[:8]  # Shorten UUID for the sake of example
    customer_number = time_str + unique_id
    customer_number = customer_number[:100]  # Adjust based on your requirement

    # Ensure this customer number is unique
    while UserProfile.objects.filter(customer_number=customer_number).exists():
        # Generate a new unique ID and customer number if it already exists
        unique_id = str(uuid.uuid4())[:8]  # Generate a new short UUID
        customer_number = time_str + unique_id
        customer_number = customer_number[:100]  # Ensure it's within the length limit

    # Create a new customer with this unique number
    return customer_number




def become_landlord(request):
    messages.info(request, 'Contact admin to become landloard before you can sell properties')
    return redirect('HouseListing:home')
# user registration function



@transaction.atomic
def register_user(request):
    if request.method == 'POST':
        print(request.POST)
        next = request.POST.get('next_signup')
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        user_type = request.POST.get('user_type')

        
        form = UserLogForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            username = username.lower()

            user.set_password(password)
            user.email = username
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # create user profile
                    UserProfile.objects.create(
                        user = user,
                        user_account_type = user_type,
                        full_name = full_name,
                        phone_number = phone_number,
                        email = username,
                        customer_number = generate_customer_number(),
                    )
                    
                    
                    mail_subject = 'Kindly Activate your Account to finish up your registration.'

                    message = render_to_string('HouseListing/acc_active_email.html', {
                        'user': user,
                        'domain': current_site_online,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })

                    to_email = form.cleaned_data.get('username')
                    from_email = 'info@aprilmanagement.pro'
                    
                    email = EmailMessage(
                        mail_subject, message,from_email, to=[to_email]
                    )

                    email.send()
                    messages.success(request, 'Account Created Successfully')
                    if next is not None and next == 'list':
                        return redirect('HouseListing:listing_dashboard')
                    elif next is not None and next == 'manage':
                        return redirect('HouseListing:dashboard')
                    elif next is not None and next == 'sale_home':
                        return redirect('HouseListing:create_listing_listing')
                    else:
                        return redirect('HouseListing:home')
        context = {
            'form': form,
        }
        print(form.errors)
        messages.warning(request, 'Error. Username already Taken Try another.')
        return redirect('HouseListing:home')
    else:
        form = UserLogForm(request.POST or None)
        context = {
            'form': form,
        }
        return redirect('HouseListing:home')

def verify_account(request, option):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        user = request.user
        email = request.user.email
        current_site = get_current_site(request)
        mail_subject = 'Kindly Activate your Account to finish up your registration.'
        message = render_to_string('HouseListing/acc_active_email.html', {
            'user': user,
            'domain': current_site_online,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })

        to_email = email
        from_email = 'info@aprilmanagement.pro'
        
        email = EmailMessage(
            mail_subject, message,from_email, to=[to_email]
        )
        email.send()
        messages.success(request, 'Verification email sent successfully. Kindly check your email address and click on the link to complete the verification.')

        if option == 'listing':
            return redirect('HouseListing:listing_dashboard')
        else:
            return redirect('HouseListing:dashboard')



def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user_profile_instance = UserProfile.objects.get(user=user)
        user_profile_instance.account_verified = True
        user_profile_instance.save()
        messages.success(request, 'Approved email Successfully')
        return redirect('HouseListing:home')
    else:
        return redirect('HouseListing:invalid_link')


def invalid_link(request):
    messages.warning(request, "Sorry, Link invalid. NB/ Link can't be used twice.")
    return redirect('HouseListing:home')


def create_profile(request, option):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        # get user
        try:
            userprofile = UserProfile.objects.get(user=request.user)

            if option == 'listing':
                messages.info(request, 'You have a profile associated to you')
                return redirect('HouseListing:listing_dashboard')
            else:
                messages.info(request, 'You have a profile associated to you')
                return redirect('HouseListing:dashboard')
        except:            
            if option == 'listing':
                my_template = 'HouseListing/default_listing_base.html'
            else:
                my_template = 'HouseListing/default_base.html'
            
            if request.method == "GET":
                context = {
                    'my_template': my_template,
                    'option': option,
                }
                return render(request, 'HouseListing/create_profile.html', context)
            elif request.method == "POST":
                full_name = request.POST.get('full_name')
                phone_number = request.POST.get('phone_number')
                user_type = request.POST.get('user_type')
                email = request.user.email


                UserProfile.objects.create(
                    user = request.user,
                    user_account_type = user_type,
                    full_name = full_name,
                    phone_number = phone_number,
                    email = email,
                    account_verified=True,
                )

                messages.success(request, 'Profile updated successfully')
                return redirect('HouseListing:listing_profile', option=option)


def edit_profile(request, side):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        # get user
        try:
            userprofile = UserProfile.objects.get(user=request.user)
            if request.method == 'GET':      
                if side == 'listing':
                    return redirect('HouseListing:listing_dashboard')
                elif side == 'management':
                    return redirect('HouseListing:dashboard')
                else:
                    return HttpResponse('Error occured')
            else:
                full_name = request.POST.get('full_name')
                phone = request.POST.get('phone')
                # account_type = request.POST.get('account_type')
                profile_image = request.FILES.get('profile_image', None)

                userprofile.full_name = full_name
                userprofile.phone_number = phone
                # userprofile.user_account_type = account_type

                if profile_image is not None:
                    userprofile.profile_image = profile_image
                    print('saved image ===================')

                userprofile.save()
                
                if side == 'listing':
                    messages.success(request, 'Profile update successfully')
                    return redirect('HouseListing:listing_profile', option='listing')
                elif side == 'management':
                    messages.success(request, 'Profile update successfully')
                    return redirect('HouseListing:listing_profile', option='management')
                else:
                    return HttpResponse('Error occured')
        except:  
            messages.warning(request, 'You need to create a profile.')
            return redirect('HouseListing:create_profile')


def download_admin_tours_excel(request):
    if not request.user.is_authenticated and request.user.is_superuser:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tour-leads.csv"'

    writer = csv.writer(response)
    writer.writerow(['property', 'full_name', 'phone', 'tour_date',
                    'message', 'visited', 'mark_as_span' ])

    users = Tours.objects.all().values_list('property', 'full_name', 'phone', 'tour_date',
                                           'message', 'visited', 'mark_as_span')
    for user in users:
        writer.writerow(user)
    return response


def download_relocation_leads_excel(request):
    if not request.user.is_authenticated and request.user.is_superuser:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tour-leads.csv"'

    writer = csv.writer(response)
    writer.writerow(['property', 'full_name', 'phone', 'email',
                    'current_town', 'employment_type', 'gross_income', 'convinient_time', 'property_rent', 'creation_date', 'completed' ])

    users = RelocationLeads.objects.all().values_list('property', 'full_name', 'phone', 'email',
                                           'current_town', 'employment_type', 'gross_income', 'convinient_time', 'property_rent', 'creation_date', 'completed')
    for user in users:
        writer.writerow(user)
    return response




def manage_create_profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        # get user
        try:
            userprofile = UserProfile.objects.get(user=request.user)
            return redirect('HouseListing:dashboard')
        except:            
            if request.method == "GET":
                return render(request, 'HouseListing/manage_create_profile.html')
            elif request.method == "POST":
                full_name = request.POST.get('full_name')
                phone_number = request.POST.get('phone_number')
                user_type = request.POST.get('user_type')
                email = request.user.email

                UserProfile.objects.create(
                    user = request.user,
                    user_account_type = user_type,
                    full_name = full_name,
                    phone_number = phone_number,
                    email = email
                )

                messages.success(request, 'Profile updated successfully')
                return redirect('HouseListing:manage_profile')



def freetrial(request):
    return render(request, 'HouseListing/default_freetrial.html')



# case system

def open_case(request, property_id):
    property = Properties.objects.get(id=property_id)
    landlord = property.user.userprofile

    open_date = request.POST.get('open_date')
    details = request.POST.get('details')
    case_number = request.POST.get('case_number')
    court = request.POST.get('court')
    jurisdiction = request.POST.get('jurisdiction')
    case_type = request.POST.get('case_type', None)
    attorney = request.POST.get('attorney')
    legal_fees = request.POST.get('legal_fees')

    legal_document = request.FILES.get('legal_document', None)

    print(landlord)

    LegalCase.objects.create(
        property = property,
        landlord = landlord,
        open_date = open_date,
        details = details,
        outcome = 'Pending',
        case_number = case_number,
        court = court,
        jurisdiction = jurisdiction,
        case_type = case_type,
        attorney = attorney,
        legal_fees = legal_fees,
        documents = legal_document,
    )

    messages.success(request, 'Case opened successfully')
    return redirect(request.META.get('HTTP_REFERER'))




def case_details(request, pk):

    court_case = LegalCase.objects.get(id=pk)
    legal_proceedings = LegalProceeding.objects.filter(legalcase=court_case)


    context = {
        'court_case': court_case,
        'legal_proceedings': legal_proceedings,    
    }
    
    return render(request, 'HouseListing/case_details.html', context)


def delete_proceeding(request, pk):
    proceeding = LegalProceeding.objects.get(id=pk)
    case = proceeding.legalcase
    proceeding.delete()
    messages.success(request, 'Proceeding deleted successfully')
    return redirect('HouseListing:case_details', pk=case.id)

def register_proceeding(request, case_id):
    case = LegalCase.objects.get(id=case_id)

    case_date = request.POST.get('date')
    notes = request.POST.get('notes')

    LegalProceeding.objects.create(
        legalcase = case,
        date = case_date,
        notes = notes
    )

    messages.success(request, 'Proceeding Created successfully')
    return redirect('HouseListing:case_details', pk=case.id)



def request_for_contract_approval(request, property_id):
    if request.method == 'POST':
        contract_service_type = request.POST.get('contract_service_type')
        contract_description = request.POST.get('contract_description')

        MaintenanceContract.objects.create(
            property = Properties.objects.get(id=property_id),
            service_type = contract_service_type,
            description = contract_description,
            open_for_bids = True,
            super_admin_approved = False,
        )

        messages.success(request, 'Contract Requested Successfully, Please wait for approval & communcation regarding the status.')
        return redirect(request.META.get('HTTP_REFERER'))
    pass

def contractor_bid_list(request):
    open_contractor_request = MaintenanceContract.objects.filter(super_admin_approved=False)
    open_for_bids = MaintenanceContract.objects.filter(super_admin_approved=True, open_for_bids=True)

    context = {
        'open_contractor_request': open_contractor_request,
        'open_for_bids': open_for_bids
    }
    return render(request, 'HouseListing/manage_contractor_bids.html', context)


def place_bid(request, contract_id):
    proposal = request.POST.get('proposal')

    Bid.objects.create(
        contract=MaintenanceContract.objects.get(id=contract_id),
        business_owner = UserProfile.objects.get(user=request.user),
        proposal_details = proposal
    )
    messages.success(request, 'Proposal submited sucessfully.')
    return redirect(request.META.get('HTTP_REFERER'))

def contract_details(request, contract_id):
    contract = MaintenanceContract.objects.get(id=contract_id)
    all_bids = Bid.objects.filter(contract=contract)
    
    print(contract)
    context = {
        'contract' :contract,
        'all_bids': all_bids
    }
    return render(request, 'HouseListing/contract_details.html', context)


def assign_to_contract(request, contract_id, bid_id):
    contract = MaintenanceContract.objects.get(id=contract_id)
    bid = Bid.objects.get(id=bid_id)

    contract.selected_bid = bid
    contract.open_for_bids = False
    contract.save()

    messages.success(request, 'Successfully assigned Contract to business owner.')
    return redirect('HouseListing:contractor_bid_list')



def approve_contract_for_bidding(request, contract_id):
    contract = MaintenanceContract.objects.get(id=contract_id)
    contract.super_admin_approved = True
    contract.open_for_bids = True
    contract.save()

    messages.success(request, 'Request approved successfull. Contractors/Business owners can now bid on this job')
    return redirect(request.META.get('HTTP_REFERER'))



def contractor_available_contracts(request):
    available_contracts_for_bidding = MaintenanceContract.objects.filter(super_admin_approved=True, open_for_bids=True).order_by('-id')

    context = {
        'available_contracts_for_bidding': available_contracts_for_bidding,
    }

    return render(request, 'HouseListing/contractor_available_contracts.html', context)

def contractor_my_contracts(request):
    my_contracts = MaintenanceContract.objects.filter(selected_bid__business_owner__user=request.user)

    context = {
        'my_contracts': my_contracts,
    }
    return render(request, 'HouseListing/my_contracts.html', context)


def financials(request):
    # so I need to get summary of all payments received batched per month per property

    all_payments = Payment.objects.all()

    # get all properties
    all_properties = Properties.objects.all()

def test_500_error(request):
    """Test view to trigger a 500 error for testing purposes"""
    # This will intentionally cause a server error
    raise Exception("This is a test 500 error for testing error handling")

