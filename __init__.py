#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.pool import Pool
from .sale import *
from .purchase import *

def register():
    Pool.register(
        Sale,
        Purchase,
        module='nodux_account_payment', type_='model')
