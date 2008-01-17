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
 *  File:            Lists.h
 *  
 *  Description:     Include file for dealing with lists.
 * 
 *  Author:          Vicente Rey
 *
 *  Created:         22 May 1995
 *  
 *    (copyright by E.S.R.F.  March 1995)
 * 
 ***************************************************************************/
#ifndef LISTS_H
#define LISTS_H

/* #include <malloc.h> */

typedef struct _ObjectList {
  struct _ObjectList   *next;
  struct _ObjectList   *prev;
  void                 *contents;
} ObjectList;

typedef struct _ListHeader {
  struct _ObjectList   *first;
  struct _ObjectList   *last;
} ListHeader;

extern  ObjectList * findInList     ( ListHeader *list, int (*proc)(void *,void *), void *value );                         
extern  long         addToList      ( ListHeader *list, void *object,long size);
extern  void         unlinkFromList ( ListHeader *list,  ObjectList *element);

#endif  /*  LISTS_H  */
