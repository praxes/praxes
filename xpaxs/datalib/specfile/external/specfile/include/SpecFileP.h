#/*##########################################################################
# Copyright (C) 2004-2006 European Synchrotron Radiation Facility
#
# This file is part of the PyMCA X-ray Fluorescence Toolkit developed at
# the ESRF by the Beamline Instrumentation Software Support (BLISS) group.
#
# This toolkit is free software; you can redistribute it and/or modify it 
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option) 
# any later version.
#
# PyMCA is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# PyMCA; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
# Suite 330, Boston, MA 02111-1307, USA.
#
# PyMCA follows the dual licensing model of Trolltech's Qt and Riverbank's PyQt
# and cannot be used as a free plugin for a non-free program. 
#
# Please contact the ESRF industrial unit (industry@esrf.fr) if this license 
# is a problem to you.
#############################################################################*/

/***************************************************************************
 *  
 *  File:            SpecFileP.h
 *  
 *  Description:     Include file for treating spec data files.
 * 
 *  Author:          Vicente Rey
 *
 *  Created:         2 March 1995
 *  
 *    (copyright by E.S.R.F.  March 1995)
 * 
 ***************************************************************************/
#ifndef SPECFILE_P_H
#define SPECFILE_P_H

/*
 * Defines.
 */
#define   FILE_HEADER         0
#define   SCAN                1

#define   FROM_SCAN           0
#define   FROM_FILE           1

#define   SF_COMMENT         'C'
#define   SF_DATE            'D'
#define   SF_EPOCH           'E'
#define   SF_FILE_NAME       'F'
#define   SF_GEOMETRY        'G'
#define   SF_INTENSITY       'I'
#define   SF_LABEL           'L'
#define   SF_MON_NORM        'M'
#define   SF_COLUMNS         'N'
#define   SF_MOTOR_NAMES     'O'
#define   SF_MOTOR_POSITIONS 'P'
#define   SF_RECIP_SPACE     'Q'
#define   SF_RESULTS         'R'
#define   SF_SCAN_NUM        'S'
#define   SF_TIME_NORM       'T'
#define   SF_USER_DEFINED    'U'
#define   SF_TEMPERATURE     'X'
#define   SF_MCA_DATA        '@'

/*
 * Library internal functions
 */
extern  int        sfSetCurrent    ( SpecFile *sf,   long index, int *error);
extern ObjectList *findScanByIndex ( ListHeader *list, long index );
extern ObjectList *findScanByNo    ( ListHeader *list, long scan_no, long order );
extern void        freeArr         ( void ***ptr, long lines );
extern void        freeAllData     ( SpecFile *sf );
extern long        mulstrtod       ( char *str, double **arr, int *error );
extern int         sfGetHeaderLine ( SpecFile *sf, int from, char character,
                                             char **buf,int *error);

#endif  /*  SPECFILE_P_H  */
