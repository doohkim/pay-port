def owner_serializer_update_method(instance, validated_data):
    instance.business_license_number = validated_data.get('business_license_number',
                                                          instance.business_license_number)
    instance.business_condition = validated_data.get('business_condition', instance.business_condition)
    instance.business_open_date = validated_data.get('business_open_date', instance.business_open_date)
    instance.business_capital_amount = validated_data.get('business_capital_amount',
                                                          instance.business_capital_amount)
    instance.business_url = validated_data.get('business_url', instance.business_url)
    instance.business_representative_name = validated_data.get('business_representative_name',
                                                               instance.business_representative_name)
    instance.business_representative_birth = validated_data.get('business_representative_birth',
                                                                instance.business_representative_birth)
    instance.business_representative_phone = validated_data.get('business_representative_phone',
                                                                instance.business_representative_phone)
    instance.business_representative_fax = validated_data.get('business_representative_fax',
                                                              instance.business_representative_fax)
    instance.business_representative_email = validated_data.get('business_representative_email',
                                                                instance.business_representative_email)
    instance.business_classification = validated_data.get('business_classification',
                                                          instance.business_classification)
    instance.business_name = validated_data.get('business_name', instance.business_name)
    instance.business_main_item = validated_data.get('business_main_item', instance.business_main_item)
    instance.application_route = validated_data.get('application_route', instance.application_route)
    instance.sales_channel = validated_data.get('sales_channel', instance.sales_channel)
    instance.transaction_amount = validated_data.get('transaction_amount', instance.transaction_amount)
    instance.past_pg_company = validated_data.get('past_pg_company', instance.past_pg_company)
    instance.business_official_address = validated_data.get('business_official_address',
                                                            instance.business_official_address)
    instance.business_real_address = validated_data.get('business_real_address', instance.business_real_address)
    instance.initial_registration_fee = validated_data.get('initial_registration_fee',
                                                           instance.initial_registration_fee)
    instance.annual_management_fee = validated_data.get('annual_management_fee', instance.annual_management_fee)
    instance.guarantee_insurance_policy = validated_data.get('guarantee_insurance_policy',
                                                             instance.guarantee_insurance_policy)
    instance.reason_exemption = validated_data.get('reason_exemption', instance.reason_exemption)
    instance.call_contents = validated_data.get('call_contents', instance.call_contents)
    instance.contact_receipt = validated_data.get('contact_receipt', instance.contact_receipt)
    instance.contact_current_status = validated_data.get('contact_current_status', instance.contact_current_status)
    instance.pdf1 = validated_data.get('pdf1', instance.pdf1)
    instance.save()
    return instance
