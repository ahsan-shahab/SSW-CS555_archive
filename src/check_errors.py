"""Module for checking for logical errors in gedcom files"""
from birth_before_death import *
from marr_before_div import *
from lt150 import *
from birth_after_marr import *
from date_before_now import *
from birth_before_marr import *
from marr_before_death import *
from divorce_before_death import *
from parents_not_too_old import *
from no_bigamy import *
from birth_before_parents_death import *
from marr_after_14 import *

def check_indiv(indivs, fams):
    """Checks for individual-level logical errors"""
    for key in sorted(indivs.iterkeys()):
        if not birth_before_now(indivs[key]):
            print "Error US01: Birth date of {} ({}) occurs in the future".format(indivs[key]['NAME'], key) 
        if not death_before_now(indivs[key]):
            print "Error US01: Death date of {} ({}) occurs in the future".format(indivs[key]['NAME'], key)
        if not birth_before_death(indivs[key]):
            if indivs[key]["SEX"] == "M": pronoun = "his"
            else: pronoun = "her"
            print "Error US03: Birth date of {} ({}) occurs after {} death date".format(indivs[key]["NAME"], key, pronoun)
        if "DEAT" in indivs[key]:
            if not check150(indivs[key]["BIRT"],indivs[key]["DEAT"]):
                print "Error US07: Age of {} greater than 150 years".format(indivs[key]["NAME"])
        if not "DEAT" in indivs[key]:
            if not check150(indivs[key]["BIRT"], None):
                print "Error US07: Age of {} is greater than 150 years".format(indivs[key]["NAME"])
        if no_bigamy(indivs[key], fams) != True:
            print ("Anomaly US11: Individual ({})'s marriage in {} overlaps with their marriage in {}"
                   .format(key, no_bigamy(indivs[key], fams)[0], no_bigamy(indivs[key], fams)[1]))

def check_fam(fams, indivs):
    """Checks for family-level logical errors"""
    for key in sorted(fams.iterkeys()):
        if not marr_before_now(fams[key]):
            print "Error US01: Marriage date of this family occurs in the future ({})".format(key)
        if not div_before_now(fams[key]):
            print "Error US01: Divorce date of this family occurs in the future ({})".format(key)
        if not birth_before_marr_husb(fams[key], indivs):
            print "Error US02: Birth date of husband occurs after marriage in this family ({})".format(key)
        if not birth_before_marr_wife(fams[key], indivs):
            print "Error US02: Birth date of wife occurs after marriage in this family ({})".format(key)
        if not marr_before_div(fams[key]):
            print "Error US04: Divorce occurs before marriage in this family ({})".format(key)
        if not marr_before_child(indivs, fams[key]):
            print "Anomaly US08: Birth of child before marriage in this family: ({})".format(key)
        if not marr_before_death_husb(fams[key], indivs):
            print "Error US05: Death date of husband occurs before marriage in this family ({})".format(key)
        if not marr_before_death_wife(fams[key], indivs):
            print "Error US05: Death date of wife occurs before marriage in this family ({})".format(key)
        if not divorce_before_death_husb(fams[key], indivs):
            print "Error US06: Death date of husband occurs before divorce in this family ({})".format(key)
        if not divorce_before_death_wife(fams[key], indivs):
            print "Error US06: Death date of wife occurs before divorce in this family ({})".format(key)
        if not husb_not_too_old(fams[key], indivs):
            print "Error US12: Husband in this family ({}) is too old to be a father.".format(key)
        if not wife_not_too_old(fams[key], indivs):
            print "Error US12: Wife in this family ({}) is too old to be a mother.".format(key)
        if not birth_before_parents_death(indivs, fams[key]):
            print "Error US09: Death of parent occurs before birth of child is possible in this family ({})".format(key)
        if not male_last_names.male_last_names(indivs, male_last_names.get_males(fams[key],indivs)):
            print "Error US16: Male surnames not consistent in this family ({})".format(key)
        if not no_marr_to_desc.no_marr_to_desc(indivs, fams[key], fams):
            print "Error US17: Marriage to descendents found: ({})".format(key)
        if not husb_marr_after_14(indivs, fams[key]):
            print "Error US10: Husband in this family ({}) was younger than 14 when married.".format(key)
        if not wife_marr_after_14(indivs, fams[key]):
            print "Error US10: Wife in this family ({}) was younger than 14 when married.".format(key)
