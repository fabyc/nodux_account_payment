# This file is part of the sale_payment module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
#! -*- coding: utf8 -*-
from decimal import Decimal
from trytond.model import ModelView, fields
from trytond.pool import PoolMeta, Pool
from datetime import datetime,timedelta
import os

__all__ = ['Purchase']
__metaclass__ = PoolMeta

class Purchase():
    __name__ = 'purchase.purchase'

    check_amount = fields.Function(fields.Numeric('Check Amount',
            readonly=True, help="Payment check amount"), 'get_check_amount', Decimal(0.0))

    cash_amount = fields.Function(fields.Numeric('Cash Amount',
            readonly=True, help="Payment cash amount"), 'get_cash_amount', Decimal(0.0))

    maturity_date = fields.Function(fields.Date('Maturity Date',
            readonly=True), 'get_maturity_date')

    state_date = fields.Function(fields.Char('State Date',
            readonly=True), 'get_state_date')

    residual_amount = fields.Function(fields.Numeric('Residual Amount',
            readonly=True,), 'get_residual_amount', Decimal(0.0))
    @classmethod
    def __setup__(cls):
        super(Purchase, cls).__setup__()

    @classmethod
    def get_check_amount(cls, purchases, names):
        pool = Pool()
        InvoiceLine = pool.get('account.invoice.line')
        Invoice = pool.get('account.invoice')
        MoveLine = pool.get('account.voucher.line')
        PaymentLine = pool.get('account.voucher.line.paymode')
        amount = Decimal(0.0)
        id_i = None
        result = {n: {s.id: Decimal(0) for s in purchases} for n in names}
        for name in names:
            for purchase in purchases:
                for line in purchase.lines:
                    lines_invoice = InvoiceLine.search([('origin','=', 'purchase.line,'+str(line.id))])
                    for l in lines_invoice:
                        id_i = l.invoice.id
                        invoices = Invoice.search([('id', '=', id_i)])
                amount = Decimal(0.0)
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
                    result[name][purchase.id] = amount
                else:
                    result[name][purchase.id] = Decimal(0.0)
        return result

    @classmethod
    def get_cash_amount(cls, purchases, names):
        pool = Pool()
        InvoiceLine = pool.get('account.invoice.line')
        Invoice = pool.get('account.invoice')
        MoveLine = pool.get('account.voucher.line')
        PaymentLine = pool.get('account.voucher.line.paymode')
        amount = Decimal(0.0)
        id_i = None
        result = {n: {s.id: Decimal(0) for s in purchases} for n in names}
        for name in names:
            for purchase in purchases:
                for line in purchase.lines:
                    lines_invoice = InvoiceLine.search([('origin','=', 'purchase.line,'+str(line.id))])
                    for l in lines_invoice:
                        id_i = l.invoice.id
                        invoices = Invoice.search([('id', '=', id_i)])
                amount = Decimal(0.0)
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
                if amount:
                    result[name][purchase.id] = amount
                else:
                    result[name][purchase.id] = Decimal(0.0)
        return result

    @classmethod
    def get_maturity_date(cls, purchases, names):
        pool = Pool()
        InvoiceLine = pool.get('account.invoice.line')
        Invoice = pool.get('account.invoice')
        MoveLine = pool.get('account.move.line')
        PaymentLine = pool.get('account.voucher.line.paymode')
        Date = pool.get('ir.date')
        id_i = None
        date = Date.today()
        result = {n: {s.id: Decimal(0) for s in purchases} for n in names}
        for name in names:
            for purchase in purchases:
                for line in purchase.lines:
                    lines_invoice = InvoiceLine.search([('origin','=', 'purchase.line,'+str(line.id))])
                    for l in lines_invoice:
                        id_i = l.invoice.id
                        invoices = Invoice.search([('id', '=', id_i)])
                amount = Decimal(0.0)
                if invoices:
                    for i in invoices:
                        move = i.move
                    lines = MoveLine.search([('move', '=', move), ('party', '!=', None), ('maturity_date', '!=', None)])
                    if lines:
                        for l in lines:
                            date = l.maturity_date

                if date:
                    result[name][purchase.id] = date
                else:
                    result[name][purchase.id] = Date.today()
        return result

    @classmethod
    def get_state_date(cls, purchases, names):
        pool = Pool()
        InvoiceLine = pool.get('account.invoice.line')
        Invoice = pool.get('account.invoice')
        MoveLine = pool.get('account.move.line')
        PaymentLine = pool.get('account.voucher.line.paymode')
        Date = pool.get('ir.date')
        date_now = Date.today()
        date = Date.today()
        result = {n: {s.id: Decimal(0) for s in purchases} for n in names}
        for name in names:
            for purchase in purchases:
                for line in purchase.lines:
                    lines_invoice = InvoiceLine.search([('origin','=', 'purchase.line,'+str(line.id))])
                    for l in lines_invoice:
                        id_i = l.invoice.id
                        invoices = Invoice.search([('id', '=', id_i)])
                amount = Decimal(0.0)
                if invoices:
                    for i in invoices:
                        move = i.move
                    lines = MoveLine.search([('move', '=', move), ('party', '!=', None), ('maturity_date', '!=', None)])
                    if lines:
                        for l in lines:
                            date = l.maturity_date
                if date < date_now:
                    print "Esta vencida"
                    result[name][purchase.id] = 'vencida'
                else:
                    result[name][purchase.id] = ''
        return result

    @classmethod
    def get_residual_amount(cls, purchases, names):
        pool = Pool()
        InvoiceLine = pool.get('account.invoice.line')
        Invoice = pool.get('account.invoice')
        MoveLine = pool.get('account.voucher.line')
        PaymentLine = pool.get('account.voucher.line.paymode')
        amount = Decimal(0.0)
        residual_amount = Decimal(0.0)
        id_i = None
        result = {n: {s.id: Decimal(0) for s in purchases} for n in names}
        for name in names:
            for purchase in purchases:
                for line in purchase.lines:
                    lines_invoice = InvoiceLine.search([('origin','=', 'purchase.line,'+str(line.id))])
                    for l in lines_invoice:
                        id_i = l.invoice.id
                        invoices = Invoice.search([('id', '=', id_i)])
                amount = Decimal(0.0)
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
                            elif 'cheque' in name_pay:
                                amount += p.pay_amount
                residual_amount = purchase.total_amount - amount
                if residual_amount:
                    result[name][purchase.id] = residual_amount
                else:
                    result[name][purchase.id] = Decimal(0.0)
        return result
