'''
This script creates a python interface to a database of fundamental X-ray
fluorescence parameters compiled by W.T. Elam, B.D. Ravel and J.R. Sieber,
published in Radiation Physics and Chemistry, 63 (2), 121 (2002). The
database is published by NIST at
http://www.cstl.nist.gov/acd/839.01/xrfdownload.html

'''
import io
import json
import os
import sqlite3
import sys

import numpy as np


def create_CK(line, edge):
    ck = edge.require_group('Coster_Kronig')
    temp = line.split()[1:]
    while temp:
        (i,j), temp = temp[:2], temp[2:]
        ck[i] = float(j)
    return ck

def create_CKtotal(line, edge):
    ck_total = edge.require_group('Coster_Kronig_total')
    temp = line.split()[1:]
    while temp:
        (i,j), temp = temp[:2], temp[2:]
        ck_total[i] = float(j)
    return ck_total

def create_photoabsorption(elamdb, element):
    data = []
    while 1:
        line = elamdb[0]

        if line.startswith('    '):
            data.append(np.fromstring(line, sep=' '))
            elamdb.pop(0)
        else:
            data = np.array(data).transpose()
            break

    photo = element.require_group('photoabsorption')
    photo['log_energy'] = data[0]
    photo['log_energy'].attrs['units'] = 'eV'
    photo['log_photoabsorption'] = data[1]
    photo['log_photoabsorption'].attrs['units'] = 'cm^2/g'
    photo['log_photoabsorption_spline'] = data[2]
    return photo

def create_scatter(elamdb, element):
    data = []
    while 1:
        line = elamdb[0]

        if line.startswith('    '):
            data.append(np.fromstring(line, sep=' '))
            elamdb.pop(0)
        else:
            data = np.array(data).transpose()
            break

    scatter = element.require_group('scatter')
    scatter['log_energy'] = data[0]
    scatter['log_energy'].attrs['units'] = 'eV'
    scatter['log_coherent_scatter'] = data[1]
    scatter['log_coherent_scatter'].attrs['units'] = 'cm^2/g'
    scatter['log_coherent_scatter_spline'] = data[2]
    scatter['log_incoherent_scatter'] = data[3]
    scatter['log_incoherent_scatter'].attrs['units'] = 'cm^2/g'
    scatter['log_incoherent_scatter_spline'] = data[4]
    return  scatter

class ElamDBCreator(object):

    def __init__(self, source, dest):
        self.source_file_name = source
        self.dest_file_name = dest

    def create_database(self, overwrite=False):
        if os.path.isfile(self.dest_file_name):
            if overwrite:
                os.remove(self.dest_file_name)
            else:
                return

        with io.open(self.source_file_name, encoding='ascii') as f:
            lines = f.readlines()
            while lines[0].startswith('/'):
                lines.pop(0)

        self.conn = sqlite3.connect(self.dest_file_name)
        self.c = self.conn.cursor()

        self.c.execute(
            '''create table elements (element_id text, atomic_number integer,
            atomic_mass real, density real)
            '''
            )
        self.c.execute(
            '''create table edges (edge_id text, element_id text,
            edge_symbol text, edge_energy real, fluorescence_yield real,
            jump_ratio real)
            '''
            )
        self.c.execute(
            '''create table lines (line_id text, element_id text,
            iupac_symbol text, siegbahn_symbol text, edge_start text,
            edge_end text, energy real, intensity real)
            '''
            )

        while lines:
            line = lines.pop(0)
            if line.startswith('Element'):
                sym, num, mw, rho = line.split()[1:]
                self.c.execute(
                    'insert into elements values (?,?,?,?)',
                    (sym, num, mw, rho)
                    )
                self.current_element = sym
            elif line.startswith('Edge'):
                label, energy, yield_, jump = line.split()[1:]
                el = self.current_element
                self.c.execute(
                    'insert into edges values (?,?,?,?,?,?)',
                    ('%s_%s' % (el, label), el, label, energy, yield_, jump)
                    )
                self.current_edge = label
            elif line.startswith('  Lines'):
                while True:
                    if lines[0].startswith('    '):
                        line = lines.pop(0)
                        iupac, siegbahn, energy, intensity = line.split()
                        end, start = iupac.split('-')
                        el = self.current_element
                        id_ = '%s_%s' % (el, iupac)
                        start = '%s_%s' % (el, start)
                        end = '%s_%s' % (el, end)
                        self.c.execute(
                            'insert into lines values (?,?,?,?,?,?,?,?)',
                            (id_, el, iupac, siegbahn, start, end, energy,
                            intensity)
                            )
                    else:
                        break
        #     elif line.startswith('  CK '):
        #         ck = create_CK(line, edge)
        #     elif line.startswith('  CKtotal'):
        #         ck_total = create_CKtotal(line, edge)
        #     elif line.startswith('Photo'):
        #         photoabsorption = create_photoabsorption(elamdb, element)
        #     elif line.startswith('Scatter'):
        #         scatter = create_scatter(elamdb, element)
        #     elif line.startswith('EndElement'):
        #         continue
        #     elif line.startswith('End'):
        #         return

        self.conn.commit()

        self.c.execute('select * from lines order by edge_end')
        for row in self.c:
            print row

        self.c.close()


if __name__ == '__main__':
    elam = ElamDBCreator('elam_physical_reference/elam.dat', 'elam.db')
    elam.create_database(overwrite=True)
