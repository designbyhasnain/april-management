from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.signals import pre_save
from django.utils.text import slugify
import random
import string


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_account_type = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.CharField(max_length=100)    
    visitorcount = models.IntegerField(default=0)
    account_verified = models.BooleanField(default=False)
    profile_image = CloudinaryField('image', blank=True, null=True)

    customer_number = models.CharField(max_length=100, blank=True, null=True)
    # new fields to setup for background checks for the landlord
    # id_card = models.FileField(blank=True, null=True)
    # social_security_number = models.CharField(max_length=100, blank=True, null=True)
    # passport_photo = models.FileField(blank=True, null=True)
    # utility_bill = models.FileField(blank=True, null=True)
    # employment_letter = models.FileField(blank=True, null=True)
    # bank_statement = models.FileField(blank=True, null=True)
    # guarantor_id_card = models.FileField(blank=True, null=True)
    # guarantor_passport_photo = models.FileField(blank=True, null=True)
    # guarantor_utility_bill = models.FileField(blank=True, null=True)
    # guarantor_employment_letter = models.FileField(blank=True, null=True)
    # guarantor_bank_statement = models.FileField(blank=True, null=True)

    



    def __str__(self):
        return self.user.username



# ===============various status include :: For rent, For sale, For lease ====================
class PropertyStatus(models.Model):
    property_status = models.CharField(max_length=600)
    description = models.CharField(max_length=600, blank=True, null=True)

    class Meta:
        """Meta definition for PropertyStatus."""

        verbose_name = 'PropertyStatus'
        verbose_name_plural = 'PropertyStatus'

    def __str__(self):
        return self.property_status


class LandSizes(models.Model):
    size = models.CharField(max_length=600)

    class Meta:
        verbose_name = 'LandSizes'
        verbose_name_plural = 'LandSizes'

    def __str__(self):
        return self.size



class EmailSubscribers(models.Model):
    email = models.CharField(max_length=600, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.email)

# ==============features include : : Air conditioners , dryer , etc
class Features(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Features'
        verbose_name_plural = 'Features'


    def __str__(self):
        return self.name



# ===========type of house ie commercial, residential etc
class Type(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# ==========agents======

class Agents(models.Model):
    agent_name = models.CharField(max_length=200)
    picture = CloudinaryField('image')
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Agents'
        verbose_name_plural = 'Agents'



    def __str__(self):
        return self.agent_name


class Cities(models.Model):
    city_name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Cities'
        verbose_name_plural = 'Cities'


    def __str__(self):
        return self.city_name

class ContractorDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    service_type = models.CharField(max_length=200)  # e.g., Plumbing, Electrical
    contact_email = models.CharField(max_length=200)  # Could be phone number, email, etc.
    contact_phone = models.CharField(max_length=200)  # Could be phone number, email, etc.
    contact_location = models.CharField(max_length=200)  # Could be phone number, email, etc.
    additional_notes = models.TextField(blank=True, null=True)
    supporting_docs = models.FileField(blank=True, null=True)
    rating = models.IntegerField(default=0)
    global_contractor = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Properties(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)    
    property_title = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(PropertyStatus, on_delete=models.CASCADE)

    units = models.IntegerField(default=0, blank=True, null=True)
    available_rooms = models.IntegerField(default=0, blank=True, null=True)
    default_house_type = models.CharField(
        max_length=100, blank=True, null=True)

    available = models.BooleanField(default=True)
    price = models.IntegerField(default=0)
    security_deposit = models.IntegerField(default=0, blank=True, null=True)
    
    area_size = models.CharField(max_length=200, blank=True, null=True)
    landsize = models.ForeignKey(LandSizes, on_delete=models.CASCADE, blank=True, null=True)

    bedrooms = models.IntegerField(default=0)
    rooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    garages = models.IntegerField(default=0)
    year_built = models.CharField(max_length=100, blank=True, null=True)

    # map
    street_name = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)

    # physica description
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    street = models.CharField(max_length=200, blank=True, null=True)
    
    # media
    video_url = models.CharField(max_length=1000, blank=True, null=True)
    virtual_tour_link = models.CharField(max_length=1000, blank=True, null=True)

    # contact 
    publish = models.BooleanField(default=True)

    managed_by_manyumba = models.BooleanField(default=False)

    featured_image = CloudinaryField('image')

    approved_by_admin = models.IntegerField(default=0, blank=True, null=True)

    uses_own_contractor = models.BooleanField(default=False)
    contractor_details = models.ForeignKey(ContractorDetails, on_delete=models.SET_NULL, null=True, blank=True)


    # amenities
    Water = models.BooleanField(default=False)
    Electricity = models.BooleanField(default=False)
    WFI = models.BooleanField(default=False)
    Ac = models.BooleanField(default=False)
    Gateman = models.BooleanField(default=False)
    Parking = models.BooleanField(default=False)
    Swimming_Pool = models.BooleanField(default=False)
    Balcony = models.BooleanField(default=False)
    Gym = models.BooleanField(default=False)
    Play_Area = models.BooleanField(default=False)
    Internet = models.BooleanField(default=False)

    ElectricSupply = models.BooleanField(default=False)
    WaterSupply = models.BooleanField(default=False)
    RainWaterDrainage = models.BooleanField(default=False)
    DomesticSewage = models.BooleanField(default=False)


    BusinessLounge = models.BooleanField(default=False)
    Majortransportlinks = models.BooleanField(default=False)
    MeetingRooms = models.BooleanField(default=False)
    CCTV = models.BooleanField(default=False)
    Elevator = models.BooleanField(default=False)

    # relevant docs

    inspection_reports = models.FileField(blank=True, null=True)
    legal_documents = models.FileField(blank=True, null=True)



    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    balance = models.FloatField(default=0, blank=True, null=True)

    class Meta:
        verbose_name = 'Properties'
        verbose_name_plural = 'Properties'


    def __str__(self):
        return self.property_title

    def return_all_units(self):
        return self.units

    def return_vacant_units(self):
        return self.available_rooms

    def calculate_occupancy(self):
        modulus =self.units -  self.available_rooms
        occupancy = (modulus / self.units) * 100
        return occupancy
    
    def return_other_images(self):
        this_property_id = self.id
        all_images = PropertyImages.objects.filter(property__id=this_property_id)
        return all_images

    def get_amenities(self):
        # Specify the amenities fields explicitly or use introspection to get them dynamically
        amenities_fields = [
            'Water', 'Electricity', 'WFI', 'Ac', 'Gateman', 'Parking',
            'Swimming_Pool', 'Balcony', 'Gym', 'Play_Area', 'Internet',
            'ElectricSupply', 'WaterSupply', 'RainWaterDrainage', 'DomesticSewage',
            'BusinessLounge', 'Majortransportlinks', 'MeetingRooms', 'CCTV', 'Elevator'
        ]
        return [(field.verbose_name, getattr(self, field.name)) for field in Properties._meta.fields if field.name in amenities_fields]


class MaintenanceContract(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=200)  # e.g., Plumbing, Electrical
    description = models.TextField()
    open_for_bids = models.BooleanField(default=True)
    super_admin_approved = models.BooleanField(default=False)
    selected_bid = models.ForeignKey('Bid', on_delete=models.SET_NULL, null=True, blank=True, related_name='selected_contract')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.service_type} for {self.property.property_title}"
    

class Bid(models.Model):
    contract = models.ForeignKey(MaintenanceContract, on_delete=models.CASCADE, related_name='bids')
    business_owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # Or a new model like BusinessProfile
    proposal_details = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(blank=True, null=True)
    


    def __str__(self):
        return f"{self.business_owner.full_name}'s bid for {self.contract}"
class RentalCriteria(models.Model):
    property = models.OneToOneField(Properties, on_delete=models.CASCADE, related_name='rental_criteria')
    minimum_income = models.CharField(max_length=1000, null=True, blank=True)
    credit_score = models.CharField(max_length=1000, null=True, blank=True)
    employment_status = models.CharField(max_length=100, null=True, blank=True)
    smoking_allowed = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)
    max_occupants = models.CharField(max_length=1000, null=True, blank=True)
    lease_duration = models.CharField(max_length=1000, null=True, blank=True)
    # Add more fields based on your criteria


class LegalCase(models.Model):
    property = models.ForeignKey(Properties , on_delete=models.CASCADE)
    landlord = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    case_number = models.CharField(max_length=100, blank=True, null=True)
    # generate fields associated to cases

    case_type = models.CharField(max_length=100, blank=True, null=True)
    legal_fees = models.CharField(max_length=100, null=True, blank=True)  # Legal fees incurred due to the case
    other_expenses = models.CharField(max_length=100, null=True, blank=True)  # Legal fees incurred due to the case
    court = models.CharField(max_length=255, null=True, blank=True)  # Court where the case is being heard, if applicable
    jurisdiction = models.CharField(max_length=100, null=True, blank=True)  # Legal jurisdiction under which the case falls
    attorney = models.CharField(max_length=255, null=True, blank=True)  # Attorney or legal firm representing the landlord
    notes = models.TextField(blank=True, null=True)  # Additional notes or remarks
    documents = models.FileField(upload_to='legal_cases/', null=True, blank=True)  # Optional: For uploading relevant documents


    open_date = models.DateField()
    details = models.TextField()
    outcome = models.CharField(max_length=255, blank=True, null=True)
    case_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self) -> str:
        return self.case_number


class LegalProceeding(models.Model):
    legalcase = models.ForeignKey(LegalCase, on_delete=models.CASCADE)
    date = models.DateField()    
    notes = models.TextField(blank=True, null=True)

    # Add any additional fields as needed

    def __str__(self):
        return f"{self.property} - {self.date}"

class Tenant(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    t_user = models.ForeignKey(User, related_name='t_user', on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=10, blank=True)
    email = models.EmailField()
    contact = models.CharField(max_length=100)
    id_card = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    # property media  


class House(models.Model):
    apartment = models.ForeignKey(Properties, on_delete=models.CASCADE)
    house_code = models.CharField(max_length=1000, blank=True, null=True)
    house_type = models.CharField(max_length=200)
    rent = models.IntegerField(default=0)
    deposit = models.IntegerField(default=0)
    arrears = models.IntegerField(default=0)
    vacant = models.BooleanField(default=True)
    house_featured_image = CloudinaryField('image')

    def __str__(self):
        return str(self.house_code)


class Lease(models.Model):
    apartment = models.ForeignKey(Properties, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    lease_start_date = models.DateField(auto_now_add=True)
    lease_end_date = models.DateField()
    lease_documents = models.FileField(blank=True, null=True)
    current_status = models.BooleanField(default=False)
    running_balance = models.FloatField(default=0, blank=True, null=True)

    credit_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overdue_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    def __str__(self):
        return str(self.id)

    def return_active_lease(self):
        return 3

class VacateNotice(models.Model):
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE)
    vacate_date = models.CharField(max_length=1000)
    remarks = models.CharField(max_length=1000, blank=True, null=True)
    vacated = models.BooleanField(default=False)
    

    def __str__(self):
        return str(self.lease)

class RepairRequest(models.Model):
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE)
    request_date = models.DateField(auto_now_add=True)
    request_deadline = models.DateField()
    request_details = models.TextField()
    request_priority = models.CharField(max_length=100)
    request_status = models.CharField(max_length=100, default='Pending')
    request_completed = models.BooleanField(default=False)
    completion_date = models.DateField(blank=True, null=True)
    completion_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.lease)
    

class Complain(models.Model):
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE)
    complain_date = models.DateField(auto_now_add=True)
    complain_details = models.TextField()
    complain_status = models.CharField(max_length=100, default='Pending')
    complain_resolved = models.BooleanField(default=False)
    resolution_date = models.DateField(blank=True, null=True)
    resolution_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.lease)
class FloorPlans(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    plan_title = models.CharField(max_length=100)
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=1)
    plan_size = models.IntegerField(default=1)
    plan_image = CloudinaryField('image', blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        verbose_name = 'FloorPlans'
        verbose_name_plural = 'FloorPlans'


    def __str__(self):
        return self.plan_title



class PropertyDocuments(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    document = models.FileField(blank=True, null=True)



class PropertyImages(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    image = CloudinaryField('image')
    home_tag = models.CharField(max_length=100)
    featured = models.BooleanField(default=False)

    class Meta:

        verbose_name = 'PropertyImages'
        verbose_name_plural = 'PropertyImages'

    def __str__(self):
        return self.home_tag
 
class AdditionalDetails(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=1000)

    class Meta:
        verbose_name = 'AdditionalDetails'
        verbose_name_plural = 'AdditionalDetails'


    def __str__(self):
        return self.title


class Invoice(models.Model):
    # apartment = models.ForeignKey(Properties, on_delete=models.CASCADE)
    # house = models.ForeignKey(House, on_delete=models.CASCADE)
    # tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE)
    amount_incurred = models.FloatField(default=0)
    fully_paid = models.BooleanField(default=False)
    date_generated = models.DateField()
    amount_paid = models.FloatField(default=0, blank=True, null=True)
    amount_due = models.FloatField(default=0, blank=True, null=True)
    previous_over_dues = models.FloatField(default=0, blank=True, null=True)
    date_paid = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

# improved Invoice
class InvoiceHybrid(models.Model):
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='invoices_hybrid')
    billing_for = models.CharField(max_length=100, blank=True, null=True)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default='Pending', choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Partial', 'Partial')])
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField()  # The month this invoice covers

    def __str__(self):
        return f"Invoice for {self.month.strftime('%B %Y')} - Lease {self.lease.id}"

class Payment(models.Model):
    invoice = models.ForeignKey(InvoiceHybrid, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100, blank=True, null=True, default='Authorize.net')

    def __str__(self):
        return f"Payment of ${self.amount_paid} on {self.date_paid.strftime('%Y-%m-%d')}"

# class PaidRent(models.Model):
#     apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
#     house = models.ForeignKey(House, on_delete=models.CASCADE)
#     lease = models.ForeignKey(
#         Lease, on_delete=models.CASCADE, blank=True, null=True)
#     tenant = models.ForeignKey(
#         Tenant, on_delete=models.CASCADE, blank=True, null=True)
#     amount_paid = models.FloatField()
#     payment_for = models.DateField(blank=True, null=True)
#     date_paid = models.DateField()

#     def __str__(self):
#         return str(self.id)


class MorgageLeads(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=100, null=True, blank='True')
    phone = models.CharField(max_length=100, null=True, blank='True')
    email = models.CharField(max_length=100, null=True, blank='True')
    employment_type = models.CharField(max_length=100, null=True, blank='True')
    gross_income = models.CharField(max_length=100, null=True, blank='True')
    convinient_time = models.CharField(max_length=100, null=True, blank='True')
    property_price = models.IntegerField(null=True, blank='True')

    class Meta:

        verbose_name = 'MorgageLeads'
        verbose_name_plural = 'MorgageLeadss'

    def __str__(self):
        return self.full_name


class RelocationLeads(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=100, null=True, blank='True')
    phone = models.CharField(max_length=100, null=True, blank='True')
    email = models.CharField(max_length=100, null=True, blank='True')
    current_town = models.CharField(max_length=100, null=True, blank='True')
    employment_type = models.CharField(max_length=100, null=True, blank='True')
    gross_income = models.CharField(max_length=100, null=True, blank='True')
    convinient_time = models.CharField(max_length=100, null=True, blank='True')
    property_rent = models.IntegerField(null=True, blank='True')
    creation_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    completed = models.BooleanField(default=False)

    class Meta:

        verbose_name = 'RelocationLeads'
        verbose_name_plural = 'RelocationLeads'

    def __str__(self):
        return self.full_name


class Tours(models.Model):

    property = models.ForeignKey(Properties, on_delete=models.CASCADE, blank=True, null=True)    
    full_name = models.CharField(max_length=1000, null=True, blank='True')
    phone = models.CharField(max_length=1000, null=True, blank='True')
    tour_date = models.CharField(max_length=1000, null=True, blank='True')
    message = models.CharField(max_length=1000, null=True, blank='True')
    visited = models.BooleanField(default=False)
    mark_as_span = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Tours'
        verbose_name_plural = 'Tours'

    def __str__(self):
        return self.full_name



def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.property_title)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug, randstr=random_string_generator(size=4))

        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def pre_save_receiver(sender, instance, *args, **kwargs):
    print(instance.slug)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_receiver, sender=Properties)
