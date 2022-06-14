from faker import Faker
import faker_commerce
import random
import datetime
import os

fake = Faker('en_US')

fake.add_provider(faker_commerce.Provider)

insert_customer_template = 'insert into customer (id, first_name, last_name, date_of_birth, phone_number, email) ' \
                           'values ({id}, \'{first_name}\', \'{last_name}\', to_date(\'{date_of_birth}\', \'YYYY-MM-DD\'), \'{phone_number}\', \'{email}\')'

insert_address_template = 'insert into address (id, building_number, street_name, city, state_abbr, postcode, customer_id) ' \
                          'values ({id}, \'{building_number}\', \'{street_name}\', \'{city}\', \'{state_abbr}\', {postcode}, {customer_id})'

insert_order_template = 'insert into order_ (id, date_, customer_id) ' \
                        'values ({}, to_timestamp(\'{}\', \'YYYY-MM-DD HH24:MI:SS\'), {})'

insert_supplier_template = 'insert into supplier (id, company, phone_number, company_email) ' \
                           'values ({id}, \'{company}\', \'{phone_number}\', \'{company_email}\')'

insert_product_template = 'insert into product (id, name_, price, supplier_id) ' \
                          'values ({id}, \'{name_}\', {price}, {supplier_id})'

insert_order_item_template = 'insert into order_item (id, quantity, order_id, product_id) ' \
                             'values ({id}, {quantity}, {order_id}, {product_id})'

customer_count = 60_000
order_count = 600_000
supplier_count = 60
product_count = 600
order_item_count = 6_000_000

service_founding_date = datetime.datetime(2010, 5, 17)

scripts_path = 'scripts'
insert_customer_filename = os.path.join(scripts_path, 'insert_customer.sql')
insert_address_filename = os.path.join(scripts_path, 'insert_address.sql')
insert_order_filename = os.path.join(scripts_path, 'insert_order.sql')
insert_supplier_filename = os.path.join(scripts_path, 'insert_supplier.sql')
insert_product_filename = os.path.join(scripts_path, 'insert_product.sql')
insert_order_item_filename = os.path.join(scripts_path, 'insert_order_item.sql')

if __name__ == '__main__':
    # customer and address
    with open(insert_customer_filename, 'w') as customer_file, open(insert_address_filename, 'w') as address_file:
        for i in range(customer_count):
            customer_file.write(insert_customer_template.format(id=i,
                                                                first_name=fake.first_name(),
                                                                last_name=fake.last_name(),
                                                                date_of_birth=fake.date_of_birth(minimum_age=18),
                                                                phone_number=fake.unique.phone_number(),
                                                                email=fake.unique.free_email()))
            address_file.write(insert_address_template.format(id=i,
                                                              building_number=fake.building_number(),
                                                              street_name=fake.street_name(),
                                                              city=fake.city(),
                                                              state_abbr=fake.state_abbr(),
                                                              postcode=fake.postcode(),
                                                              customer_id=i))
            customer_file.write(';\n')
            address_file.write(';\n')

    # order
    with open(insert_order_filename, 'w') as file:
        for i in range(order_count):
            file.write(insert_order_template.format(id=i,
                                                    date_=fake.date_time_between(start_date=service_founding_date),
                                                    customer_id=random.randint(0, customer_count - 1)))
            file.write(';\n')

    # supplier
    with open(insert_supplier_filename, 'w') as file:
        for i in range(supplier_count):
            file.write(insert_supplier_template.format(id=i,
                                                       company=fake.unique.company(),
                                                       phone_number=fake.unique.phone_number(),
                                                       company_email=fake.unique.company_email()))
            file.write(';\n')

    # product
    with open(insert_product_filename, 'w') as file:
        for i in range(product_count):
            file.write(insert_product_template.format(id=i,
                                                      name_=fake.unique.ecommerce_name(),
                                                      price=random.randint(1, 1200),
                                                      supplier_id=random.randint(0, supplier_count - 1)))
            file.write(';\n')

    # order item
    with open(insert_order_item_filename, 'w') as file:
        for i in range(order_item_count):
            file.write(insert_order_item_template.format(id=i,
                                                         quantity=random.randint(1, 3),
                                                         order_id=random.randint(0, order_count - 1),
                                                         product_id=random.randint(0, product_count - 1)))
            file.write(';\n')
