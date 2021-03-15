def settlement_info_serializer_update_method(instance, validated_data):
    instance.electronic_tax_invoice_email = validated_data.get('electronic_tax_invoice_email',
                                                               instance.electronic_tax_invoice_email)
    instance.settlement_use_or_not = validated_data.get('settlement_use_or_not', instance.settlement_use_or_not)
    instance.fee_settlement_standard = validated_data.get('fee_settlement_standard', instance.fee_settlement_standard)
    instance.fee_calculation_criteria = validated_data.get('fee_calculation_criteria',
                                                           instance.fee_calculation_criteria)
    instance.fee_registration_criteria = validated_data.get('fee_registration_criteria',
                                                            instance.fee_registration_criteria)
    instance.debt_offset_use_or_not = validated_data.get('debt_offset_use_or_not',
                                                         instance.debt_offset_use_or_not)
    instance.cancel_function = validated_data.get('cancel_function', instance.cancel_function)
    instance.settlement_type = validated_data.get('settlement_type', instance.settlement_type)
    instance.settlement_method = validated_data.get('settlement_method', instance.settlement_method)
    instance.restriction_on_cancellation_use_or_not = validated_data.get('restriction_on_cancellation_use_or_not',
                                                                         instance.restriction_on_cancellation_use_or_not)
    instance.pending_amount_for_each_case = validated_data.get('pending_amount_for_each_case',
                                                               instance.pending_amount_for_each_case)
    instance.classification_of_issuing_tax_invoices = validated_data.get('classification_of_issuing_tax_invoices',
                                                                         instance.classification_of_issuing_tax_invoices)
    instance.standard_for_issuance_of_tax_invoice = validated_data.get('standard_for_issuance_of_tax_invoice',
                                                                       instance.standard_for_issuance_of_tax_invoice)
    instance.save()
    return instance


def payment_method_serializer_update_method(instance, validated_data):
    instance.method_type = validated_data.get('method_type',
                                              instance.method_type)
    instance.service_use_or_not = validated_data.get('service_use_or_not', instance.service_use_or_not)
    instance.service_join_date = validated_data.get('service_join_date', instance.service_join_date)
    instance.store_type = validated_data.get('store_type', instance.store_type)
    instance.authentication_method = validated_data.get('authentication_method', instance.authentication_method)
    instance.partial_cancellation_or_not = validated_data.get('partial_cancellation_or_not',
                                                              instance.partial_cancellation_or_not)
    instance.payment_use_or_not = validated_data.get('payment_use_or_not', instance.payment_use_or_not)
    instance.shipping_destination_use_or_not = validated_data.get('shipping_destination_use_or_not',
                                                                  instance.shipping_destination_use_or_not)
    instance.offline_cat_id = validated_data.get('offline_cat_id', instance.offline_cat_id)
    instance.card_information_save_use_or_not = validated_data.get('card_information_save_use_or_not',
                                                                   instance.card_information_save_use_or_not)
    instance.save()
    return instance
