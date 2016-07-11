# This file is part of the sale_payment module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
#! -*- coding: utf8 -*-
from decimal import Decimal
from trytond.model import ModelView, fields
from trytond.pool import PoolMeta, Pool
from datetime import datetime,timedelta
import os

__all__ = ['Sale']
__metaclass__ = PoolMeta

class Sale():
    __name__ = 'sale.sale'

    check_amount = fields.Function(fields.Numeric('Check Amount',
            readonly=True, help="Payment check amount"), 'get_check_amount', Decimal(0.0))

    cash_amount = fields.Function(fields.Numeric('Cash Amount',
            readonly=True, help="Payment cash amount"), 'get_cash_amount', Decimal(0.0))

    maturity_date = fields.Function(fields.Date('Maturity Date',
            readonly=True), 'get_maturity_date')

    state_date = fields.Function(fields.Char('State Date',
            readonly=True), 'get_state_date')

    @classmethod
    def __setup__(cls):
        super(Sale, cls).__setup__()

    @classmethod
    def view_attributes(cls):
        Date = pool.get('ir.date')
        date = Date.today()
        return [('/tree', 'colors',
                If(Eval('maturity_date') < date,
                    'red'))]
    @classmethod
    def get_check_amount(cls, sales, names):
        pool = Pool()
        Invoice = pool.get('account.invoice')
        MoveLine = pool.get('account.voucher.line')
        PaymentLine = pool.get('account.voucher.line.paymode')
        amount = Decimal(0.0)
        id_i = None
        result = {n: {s.id: Decimal(0) for s in sales} for n in names}
        for name in names:
            for sale in sales:
                amount = Decimal(0.0)
                invoices = Invoice.search([('description','=', sale.reference), ('description', '!=', None)])
                if invoices:
                    for i in invoices:
                        invoice = i.number
                    move_lines = MoveLine.search([
                            ('name', '=', invoice),
                        ])
                    for line in move_lines:
                        payment_all = PaymentLine.search([('voucher', '=', line.voucher.id)])
                        for p in payment_all:
                            name_pay = p.pay_mode.name.lower()
                            if 'cheque' in name_pay:
                                amount += p.pay_amount
                if amount:
                    result[name][sale.id] = amount
                else:
                    result[name][sale.id] = Decimal(0.0)
        return result

    @classmethod
    def get_cash_amount(cls, sales, names):
        pool = Pool()
        Invoice = pool.get('account.invoice')
        MoveLine = pool.get('account.voucher.line')
        PaymentLine = pool.get('account.voucher.line.paymode')
        amount = Decimal(0.0)
        id_i = None
        result = {n: {s.id: Decimal(0) for s in sales} for n in names}
        for name in names:
            for sale in sales:
                amount = Decimal(0.0)
                invoices = Invoice.search([('description','=', sale.reference), ('description', '!=', None)])
                if invoices:
                    for i in invoices:
                        invoice = i.number
                    move_lines = MoveLine.search([
                            ('name', '=', invoice),
                        ])
                    for line in move_lines:
                        payment_all = PaymentLine.search([('voucher', '=', line.voucher.id)])
                        for p in payment_all:
                            name_pay = p.pay_mode.name.lower()
                            if 'efectivo' in name_pay:
                                amount += p.pay_amount
                for payment in sale.payments:
                    amount += payment.amount

                if amount:
                    result[name][sale.id] = amount
                else:
                    result[name][sale.id] = Decimal(0.0)
        return result

    @classmethod
    def get_maturity_date(cls, sales, names):
        pool = Pool()
        Invoice = pool.get('account.invoice')
        MoveLine = pool.get('account.move.line')
        PaymentLine = pool.get('account.voucher.line.paymode')
        Date = pool.get('ir.date')
        id_i = None
        date = Date.today()
        result = {n: {s.id: Decimal(0) for s in sales} for n in names}
        for name in names:
            for sale in sales:
                amount = Decimal(0.0)
                invoices = Invoice.search([('description','=', sale.reference), ('description', '!=', None)])
                if invoices:
                    for i in invoices:
                        move = i.move
                    lines = MoveLine.search([('move', '=', move), ('party', '!=', None), ('maturity_date', '!=', None)])
                    if lines:
                        for l in lines:
                            date = l.maturity_date

                if date:
                    result[name][sale.id] = date
                else:
                    result[name][sale.id] = Date.today()
        return result

    @classmethod
    def get_state_date(cls, sales, names):
        pool = Pool()
        Invoice = pool.get('account.invoice')
        MoveLine = pool.get('account.move.line')
        PaymentLine = pool.get('account.voucher.line.paymode')
        Date = pool.get('ir.date')
        date_now = Date.today()
        date = Date.today()
        result = {n: {s.id: Decimal(0) for s in sales} for n in names}
        for name in names:
            for sale in sales:
                amount = Decimal(0.0)
                invoices = Invoice.search([('description','=', sale.reference), ('description', '!=', None)])
                if invoices:
                    for i in invoices:
                        move = i.move
                    lines = MoveLine.search([('move', '=', move), ('party', '!=', None), ('maturity_date', '!=', None)])
                    if lines:
                        for l in lines:
                            date = l.maturity_date

                if date < date_now:
                    result[name][sale.id] = 'vencida'
                else:
                    result[name][sale.id] = ''
        return result
