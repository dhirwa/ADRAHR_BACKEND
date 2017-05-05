from app.model.models import *
from app.controller.exellento import Excellento
from app.controller.checker import Checker
from sqlalchemy.exc import IntegrityError
import xlwt
from xlrd import open_workbook
from app.controller.uniqid import uniqid
from app.controller.sector_id import sector_id


class Excellentodb:
    def __init__(self, file):
        self.file = file
        self.json_data = Excellento(self.file).json()

    def todb(self):

        for data in self.json_data:
            try:
                s_id = sector_id(data['sector'], data['district'])
                saving = SavingGroup(
                    name=data['saving_group_name'],
                    year=data['sgs_year_of_creation'],
                    member_female=data['sgs_members__female'],
                    member_male=data['sgs_members__male_'],
                    sector_id=s_id,
                    sector_name=None,
                    district_name=None,
                    sg_status=data['sgs_status_(supervised/graduated)'],
                    regDate=None
                )
                db.session.add(saving)
                db.session.commit()
            except IntegrityError:
                db.session().rollback()
                saving = SavingGroup.query.filter_by(name=data['saving_group_name']).first()

            # Amount

            saving_amount = data['saved_amount']
            if data['saved_amount'] == 'N/A':
                saving_amount = -1

            borrowing_amount = data['outstanding_loans']
            if data['outstanding_loans'] == 'N/A':
                borrowing_amount = -1

            amount = Amount(
                saving= saving_amount,
                borrowing=borrowing_amount,
                year=data['year_amount'],
                sg_id=saving.id
            )

            db.session.add(amount)
            db.session.commit()

            # International NGO

            try:
                ngo = Ngo(
                    name=data['international_ngo'].upper(),
                    email=None,
                    telephone=None,
                    website=None,
                    category=1,
                    picture=None,
                    address=None
                )

                db.session.add(ngo)
                db.session.commit()
                intl_ngo_id = ngo.id

            except IntegrityError:
                db.session().rollback()
                ngo = Ngo.query.filter_by(name=data['international_ngo'].upper()).first()
                intl_ngo_id = ngo.id

            # Local NGO

            try:
                ngo = Ngo(
                    name=data['local_ngo'].upper(),
                    email=None,
                    telephone=None,
                    website=None,
                    category=0,
                    picture=None,
                    address=None
                )

                db.session.add(ngo)
                db.session.commit()

                local_ngo_id = ngo.id

            except IntegrityError:
                db.session().rollback()
                ngo = Ngo.query.filter_by(name=data['local_ngo'].upper()).first()
                local_ngo_id = ngo.id

            # SGS

            sgs = Sgs(
                partner_id=local_ngo_id,
                funding_id=intl_ngo_id,
                sg_id=saving.id
            )

            db.session.add(sgs)
            db.session.commit()

        return 1

    def toexcel(self):
        wb = open_workbook(self.file)
        book = xlwt.Workbook()

        # add new colour to palette and set RGB colour value
        xlwt.add_palette_colour("custom_colour", 0x21)
        book.set_colour_RGB(0x21, 255,0,0)

        # now you can use the colour in styles
        sheet1 = book.add_sheet('Sheet 1')
        style = xlwt.easyxf('pattern: pattern solid, fore_colour custom_colour')

        error_file = True

        for sheet in wb.sheets():
            rows = sheet.nrows
            columns = sheet.ncols
            indexes = [0,1,2,5,11,12]
            keys = ['province', 'district', 'sector', 'member', 'saved', 'borrow']

            #header

            for row in range(0, 1):
                for col in range(columns):
                    value = sheet.cell(row, col).value
                    check_value = Checker(value).empty()
                    if check_value:
                        sheet1.write(row, col, value)
                    else:
                        sheet1.write(row, col, value, style)

            #value

            for row in range(1, rows):

                cols_value = [
                    sheet.cell(row, 0).value,
                    sheet.cell(row, 1).value,
                    sheet.cell(row, 2).value,
                    sheet.cell(row, 5).value,
                    sheet.cell(row, 11).value,
                    sheet.cell(row, 12).value
                ]

                func = [
                    Checker(cols_value[0]).province(),
                    Checker(cols_value[1]).district(),
                    Checker(cols_value[2]).sector(),
                    Checker(cols_value[3]).member(),
                    Checker(cols_value[4]).saved(),
                    Checker([cols_value[4], cols_value[5]]).borrow()
                ]



                for col in range(columns):
                    value = sheet.cell(row, col).value
                    if col not in indexes:
                        check_value = Checker(value).empty()
                        if check_value:
                            sheet1.write(row, col, value)
                        else:
                            sheet1.write(row, col, value, style)
                            error_file = False

                for i in range(len(func)):
                    if func[i]:
                        sheet1.write(row, indexes[i], cols_value[i])
                    else:
                        sheet1.write(row, indexes[i], cols_value[i], style)
                        error_file = False

        if error_file:
            json_data = self.json_data
            return [1,json_data]
        else:
            filename = uniqid() + ".xls"
            save = "/Users/muhireremy/cartix/uploads/save/" + filename
            #save = "/home/www/cartix/uploads/save/" + filename
            download = "http://api.cartix.io/api/v1/save/" + filename
            book.save(save)
            return [0,download]
