
from django.urls import path
from . import views
app_name = 'HouseListing'
urlpatterns = [


    path('populateDbWithCities/', views.populateDbWithCities,
         name='populateDbWithCities'),
    # listing urls
    path('listing_dashboard/', views.listing_dashboard, name='listing_dashboard'),
    path('create_listing_listing/', views.create_listing_listing,
         name='create_listing_listing'),
    path('my_listing/', views.my_listing, name='my_listing'),
    path('mylisting_detail/<int:pk>/',
         views.mylisting_detail, name='mylisting_detail'),
    path('togglePublish/<int:pk>/', views.togglePublish, name='togglePublish'),
    path('listing_profile/<str:option>/',
         views.listing_profile, name='listing_profile'),
    path('listing_delete_property/<int:pk>/',
         views.listing_delete_property, name='listing_delete_property'),
    path('edit_mylisting/<int:pk>/<str:side>/',
         views.edit_mylisting, name='edit_mylisting'),


    #     edit profile
    path('edit_profile/<str:side>/', views.edit_profile, name='edit_profile'),
    path('approve_listing/', views.approve_listing, name='approve_listing'),
    path('admin_morgage_leads/', views.admin_morgage_leads,
         name='admin_morgage_leads'),
    path('approve_property_detail/<int:pk>/',
         views.approve_property_detail, name='approve_property_detail'),
    path('approve_property/<int:pk>/',
         views.approve_property, name='approve_property'),
    path('reject_property/<int:pk>/',
         views.reject_property, name='reject_property'),

    path('property_details/<int:pk>/',
         views.property_details, name='property_details'),
    path('home/', views.coming_soon, name='coming_soon'),
    path('', views.home, name='home'),
    path('register_subscriber/', views.register_subscriber,
         name='register_subscriber'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('properties/', views.properties, name='properties'),
    path('create_listing/', views.create_listing, name='create_listing'),
    path('listing_details/<slug:slug>/',
         views.listing_details, name='listing_details'),
    path('listings_for_sale/', views.listings_for_sale, name='listings_for_sale'),
    path('listings_for_rent/', views.listings_for_rent, name='listings_for_rent'),
    path('listings_abroad/', views.listings_abroad, name='listings_abroad'),
    path('news_letter_subscrptions/', views.news_letter_subscrptions, name='news_letter_subscrptions'),


    path('download_admin_tours_excel/', views.download_admin_tours_excel, name='download_admin_tours_excel'),
    path('download_relocation_leads_excel/', views.download_relocation_leads_excel, name='download_relocation_leads_excel'),

    # home page search tabs
    path('search_property_for_sale/', views.search_property_for_sale,
         name='search_property_for_sale'),
    path('search_property_for_rent/', views.search_property_for_rent,
         name='search_property_for_rent'),
    path('search_property_for_lease/', views.search_property_for_lease,
         name='search_property_for_lease'),
    path('search_listing_town/<str:town>/',
         views.search_listing_town, name='search_listing_town'),

    # base urls
    path('houses_for_sale/', views.return_houses_for_sale,
         name='return_houses_for_sale'),
    path('houses_q/<str:form_filter_page>/<str:listing_status>/', views.filter_return_houses,
         name='filter_return_houses'),

    #
    path('sort_price/<str:form_filter_page>/<str:listing_status>/', views.sort_price,
         name='sort_price'),
    path('houses_for_rent/', views.return_houses_for_rent,
         name='return_houses_for_rent'),
    path('apartments_for_sale/', views.return_apartments_for_sale,
         name='return_apartments_for_sale'),
    path('apartments_for_rent/', views.return_apartments_for_rent,
         name='return_apartments_for_rent'),
    path('land_for_sale/', views.return_land_for_sale,
         name='return_land_for_sale'),
    path('commercial_properties_for_sale/', views.return_commercial_for_sale,
         name='return_commercial_for_sale'),
    path('commercial_properties_for_rent/', views.return_commercial_for_rent,
         name='return_commercial_for_rent'),

    # sanitize
    path('sanitize/', views.sanitize, name='sanitize'),

    path('house_details/<int:pk>/', views.house_details, name='house_details'),
    path('update_house/<int:pk>/', views.update_house, name='update_house'),
    path('register_tenant/', views.register_tenant, name='register_tenant'),

    #   morgage lead
    path('mortgages_leads/<int:price>/<int:pk>/',
         views.mortgages_leads, name='mortgages_leads'),
    path('create_morgage_lead/<int:pk>/',
         views.create_morgage_lead, name='create_morgage_lead'),

    path('mortage_loans', views.mortage_loans, name='mortage_loans'),
    path('mortage_loans_details', views.mortage_loans_details, name='mortage_loans_details'),
    path('mortage_relocation', views.mortage_relocation, name='mortage_relocation'),

#     relocation leads
    path('create_loan_relocation_lead/', views.create_loan_relocation_lead, name='create_loan_relocation_lead'),
    path('create_loan_relocation_lead_detail/<int:pk>/', views.create_loan_relocation_lead_detail, name='create_loan_relocation_lead_detail'),
    path('create_loan_relocation_lead_with_prop/<int:pk>/', views.create_loan_relocation_lead_with_prop, name='create_loan_relocation_lead_with_prop'),

    # tour schedule
    path('schedule_tour/<int:pk>/', views.schedule_tour, name='schedule_tour'),
    path('admin_tours/', views.admin_tours, name='admin_tours'),
    path('mark_tour_as_complete/<int:pk>/',
         views.mark_tour_as_complete, name='mark_tour_as_complete'),
    path('mark_tour_as_spam/<int:pk>/',
         views.mark_tour_as_spam, name='mark_tour_as_spam'),

     #new paths
     path('all_agents/', views.all_agents, name='all_agents'),
     path('agent_details/<int:pk>/', views.agent_details, name="agent_details"),

     path('all_cases/', views.all_cases, name='all_cases'),
    # categories
    path('property_categories/', views.property_categories,
         name='property_categories'),
    path('delete_property_category/<int:pk>/',
         views.delete_property_category, name='delete_property_category'),
    path('edit_property_categories/<int:pk>/',
         views.edit_property_categories, name='edit_property_categories'),

    # types
    path('property_type/', views.property_type, name='property_type'),
    path('delete_property_type/<int:pk>/',
         views.delete_property_type, name='delete_property_type'),
    path('edit_property_edit/<int:pk>/',
         views.edit_property_edit, name='edit_property_edit'),

    # cities
    path('property_cities/', views.property_cities, name='property_cities'),
    path('delete_property_city/<int:pk>/',
         views.delete_property_city, name='delete_property_city'),
    path('edit_property_city/<int:pk>/',
         views.edit_property_city, name='edit_property_city'),

    #     land_sizes
    path('land_sizes/', views.land_sizes, name='land_sizes'),
    path('edit_land_sizes/<int:pk>/',
         views.edit_land_sizes, name='edit_land_sizes'),
    path('delete_land_size/<int:pk>/',
         views.delete_land_size, name='delete_land_size'),
     
     # management side
     path('management_invoices/', views.management_invoices, name='management_invoices'),
     path('landloard_repair_list/', views.landloard_repair_list, name='landloard_repair_list'),
     path('landloard_tenant_complaints/', views.landloard_tenant_complaints, name='landloard_tenant_complaints'),
     path('resolve_complaint/<int:pk>/', views.resolve_complaint, name='resolve_complaint'),



    #  lease
    path('register_lease/', views.register_lease, name='register_lease'),
    path('load_houses', views.load_houses, name='load_houses'),
    path('load_tenants', views.load_tenants, name='load_tenants'),
    path('lease_list', views.lease_list, name='lease_list'),
    path('lease_details/<int:pk>/', views.lease_details, name='lease_details'),
    path('terminate_lease/<int:pk>/',
         views.terminate_lease, name='terminate_lease'),

     

    path('create_user/', views.create_user, name='create_user'),

    # invoice
    # path('invoice_list/<int:pk>/', views.invoice_list, name='invoice_list'),


    # tenants
    path('tenants_list/', views.tenants_list, name='tenants_list'),
    path('tenant_sub_list/<int:pk>/',
         views.tenant_sub_list, name='tenant_sub_list'),
    path('tenant_details/<int:pk>/', views.tenant_details, name='tenant_details'),
    path('edit_tenant/<int:pk>/', views.edit_tenant, name='edit_tenant'),
    path('tenant_change_password/', views.tenant_change_password, name='tenant_change_password'),


    # admin urls
    path('admin_listed_properties/', views.admin_listed_properties,
         name='admin_listed_properties'),
    path('admin_managed_properties/', views.admin_managed_properties,
         name='admin_managed_properties'),
    path('admin_listed_managed_properties/', views.admin_listed_managed_properties,
         name='admin_listed_managed_properties'),

    path('admin_relocation_leads/', views.admin_relocation_leads,
          name='admin_relocation_leads'),

    path('relocation_lead_complete/<int:pk>/', views.relocation_lead_complete, name='relocation_lead_complete'),

    # authentication
    path('login_user/', views.login_user, name='login_user'),
    path('login_demo/', views.login_demo, name='login_demo'),
    path('login_contractor/', views.login_contractor, name='login_contractor'),
    path('login_tenant_demo/', views.login_tenant_demo, name='login_tenant_demo'),
    path('demo_logout/', views.demo_logout, name='demo_logout'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('register_user/', views.register_user, name='register_user'),
    path('activate/<slug:uidb64>/<slug:token>/',
         views.activate, name='activate'),

    path('invalid_link/', views.invalid_link, name='invalid_link'),
    path('verify_account/<str:option>/',
         views.verify_account, name='verify_account'),
    path('create_profile/<str:option>/',
         views.create_profile, name='create_profile'),
    path('manage_create_profile/', views.manage_create_profile,
         name='manage_create_profile'),
    path('manage_profile/', views.manage_profile, name='manage_profile'),

    path('freetrial/', views.freetrial, name='freetrial'),


#     tenant
     path('tenant_dashboard/', views.tenant_dashboard, name='tenant_dashboard'),
     path('vacation_notice/', views.vacation_notice, name='vacation_notice'),
     path('vacate_notice_list/', views.vacate_notice_list, name='vacate_notice_list'),
     path('tenant_properties/', views.tenant_properties, name='tenant_properties'),
     path('tenant_property_details/<int:pk>/', views.tenant_property_details, name='tenant_property_details'),
     path('tenant_invoices/', views.tenant_invoices, name='tenant_invoices'),  
     path('invoice_template/<str:pk>/', views.invoice_template, name='invoice_template'),
     path('pay_rent_list/', views.pay_rent_list, name='pay_rent_list'),
    path('pay_rent_form/<int:pk>/', views.pay_rent_form, name='pay_rent_form'),
    path('tenant_request_repair/<str:r_type>/', views.tenant_request_repair, name='tenant_request_repair'),
    path('tenant_request_repair_details/<int:pk>/<str:r_type>/', views.tenant_request_repair_details, name='tenant_request_repair_details'),
    

    path('submit_repair_request/<int:lease_id>/', views.submit_repair_request, name='submit_repair_request'),
    path('submit_tenant_complain/<int:lease_id>/', views.submit_tenant_complain, name='submit_tenant_complain'),
    


#     contractors
     path('contractor_available_contracts/', views.contractor_available_contracts, name="contractor_available_contracts"),
     path('place_bid/<int:contract_id>/', views.place_bid, name='place_bid'),
     path('contract_details/<int:contract_id>/', views.contract_details, name='contract_details'),
     path('assign_to_contract/<int:contract_id>/<int:bid_id>/', views.assign_to_contract, name="assign_to_contract"),

     path('contractor_my_contracts/', views.contractor_my_contracts, name='contractor_my_contracts'),


    path('become_landlord/', views.become_landlord, name='become_landlord'),
    path('open_case/<int:property_id>/', views.open_case, name='open_case'),
    path('case_details/<int:pk>/', views.case_details, name='case_details'),
    path('delete_proceeding/<int:pk>/', views.delete_proceeding, name='delete_proceeding'),
    path('register_proceeding/<int:case_id>/', views.register_proceeding, name='register_proceeding'),
    path('request_for_contract_approval/<int:property_id>/', views.request_for_contract_approval, name='request_for_contract_approval'),
    path('contractor_bid_list/', views.contractor_bid_list, name='contractor_bid_list'),
    path('approve_contract_for_bidding/<int:contract_id>/', views.approve_contract_for_bidding, name="approve_contract_for_bidding"),

    path('generate_monthly_invoices/', views.generate_monthly_invoices, name='generate_monthly_invoices'),
    path('pay_rent/<int:lease_id>/<int:amount_paid>/', views.pay_rent, name='pay_rent'),
    path('payment_token_view/<int:pk>/', views.payment_token_view, name='payment_token_view'),
    path('manage_payments/', views.manage_payments, name='manage_payments'),
    path('financials/', views.financials, name='financials'),

    # Test error handling
    path('test-500-error/', views.test_500_error, name='test_500_error'),

]
