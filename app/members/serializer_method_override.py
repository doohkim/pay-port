def franchisee_update_method(instance, validated_data):
    instance.mid = validated_data.get('mid', instance.mid)
    instance.gid = validated_data.get('gid', instance.gid)
    instance.mid_name = validated_data.get('mid_name', instance.mid_name)
    instance.main_homepage = validated_data.get('main_homepage', instance.main_homepage)
    instance.sub_homepage = validated_data.get('sub_homepage', instance.sub_homepage)
    instance.is_active = validated_data.get('is_active', instance.is_active)
    instance.user_type = validated_data.get('user_type', instance.user_type)
    instance.boss_name = validated_data.get('boss_name', instance.boss_name)
    instance.email = validated_data.get('email', instance.email)
    instance.phone_number = validated_data.get('phone_number', instance.phone_number)
    instance.fax_number = validated_data.get('fax_number', instance.fax_number)
    instance.store_modified_date = validated_data.get('store_modified_date', instance.store_modified_date)
    instance.transfer_or_not = validated_data.get('transfer_or_not', instance.transfer_or_not)
    instance.published_or_not = validated_data.get('published_or_not', instance.published_or_not)
    instance.pay_link_or_not = validated_data.get('pay_link_or_not', instance.pay_link_or_not)
    instance.pg_info_auto_save_or_not = validated_data.get('pg_info_auto_save_or_not',
                                                           instance.pg_info_auto_save_or_not)
    instance.delivery_pay_or_not = validated_data.get('delivery_pay_or_not', instance.delivery_pay_or_not)
    instance.save()

    return instance


def pay_go_manager_update_method(instance, validated_data):
    print('validated_data', validated_data)
    instance.name = validated_data.get('name', instance.name)
    print(instance.name)
    instance.department = validated_data.get('department', instance.department)
    instance.position = validated_data.get('position', instance.position)
    instance.phone_number = validated_data.get('phone_number', instance.phone_number)
    instance.email = validated_data.get('email', instance.email)
    instance.save()
    return instance


def memo_update_method(instance, validated_data):
    instance.sales_slip = validated_data.get('sales_slip', instance.sales_slip)
    instance.vat_notation = validated_data.get('vat_notation', instance.vat_notation)
    instance.payment_notice = validated_data.get('payment_notice', instance.payment_notice)
    instance.modify_text = validated_data.get('modify_text', instance.modify_text)
    instance.save()

    return instance
