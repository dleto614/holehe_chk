<<<<<<< HEAD
"""
Email OSINT Tool - Checks if an email address is registered on various websites and services.
"""

=======
>>>>>>> 63af29e3f66952549618736a5574588301c05b28
import trio
import httpx
import json
import argparse
<<<<<<< HEAD
import importlib
import logging
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Configuration
SITE_MODULES = [
    # Social Media
    "holehe.modules.social_media.discord",
    "holehe.modules.social_media.instagram",
    "holehe.modules.social_media.twitter",
    "holehe.modules.social_media.snapchat",
    "holehe.modules.social_media.bitmoji",
    "holehe.modules.social_media.crevado",
    "holehe.modules.social_media.fanpop",
    "holehe.modules.social_media.imgur",
    "holehe.modules.social_media.myspace",
    "holehe.modules.social_media.parler",
    "holehe.modules.social_media.patreon",
    "holehe.modules.social_media.pinterest",
    "holehe.modules.social_media.plurk",
    "holehe.modules.social_media.strava",
    "holehe.modules.social_media.taringa",
    "holehe.modules.social_media.tellonym",
    "holehe.modules.social_media.tumblr",
    "holehe.modules.social_media.vsco",
    "holehe.modules.social_media.wattpad",
    "holehe.modules.social_media.xing",
    
    # CMS
    "holehe.modules.cms.gravatar",
    "holehe.modules.cms.atlassian",
    "holehe.modules.cms.wordpress",
    "holehe.modules.cms.voxmedia",
    
    # Company
    "holehe.modules.company.aboutme",
    
    # CRM
    "holehe.modules.crm.amocrm",
    "holehe.modules.crm.axonaut",
    "holehe.modules.crm.hubspot",
    "holehe.modules.crm.insightly",
    "holehe.modules.crm.nimble",
    "holehe.modules.crm.nocrm",
    "holehe.modules.crm.nutshell",
    "holehe.modules.crm.pipedrive",
    "holehe.modules.crm.teamleader",
    "holehe.modules.crm.zoho",
    
    # Crowdfunding
    "holehe.modules.crowfunding.buymeacoffee",
    
    # Jobs
    "holehe.modules.jobs.coroflot",
    "holehe.modules.jobs.freelancer",
    "holehe.modules.jobs.seoclerks",
    
    # Learning
    "holehe.modules.learning.diigo",
    "holehe.modules.learning.quora",
    
    # Mail Services
    "holehe.modules.mails.google",
    "holehe.modules.mails.laposte",
    "holehe.modules.mails.protonmail",
    "holehe.modules.mails.yahoo",
    
    # Media Platforms
    "holehe.modules.medias.ello",
    "holehe.modules.medias.flickr",
    "holehe.modules.medias.komoot",
    "holehe.modules.medias.rambler",
    "holehe.modules.medias.sporcle",
    
    # Medical
    "holehe.modules.medical.caringbridge",
    "holehe.modules.medical.sevencups",
    
    # Music
    "holehe.modules.music.soundcloud",
    "holehe.modules.music.spotify",
    
    # OSINT
    "holehe.modules.osint.rocketreach",
    
    # Payment
    "holehe.modules.payment.venmo",
    
    # Adult Content
    "holehe.modules.porn.pornhub",
    "holehe.modules.porn.redtube",
    "holehe.modules.porn.xnxx",
    "holehe.modules.porn.xvideos",
    
    # Productivity
    "holehe.modules.productivity.evernote",
    "holehe.modules.productivity.anydo",
    
    # Products
    "holehe.modules.products.eventbrite",
    "holehe.modules.products.nike",
    
    # Programming
    "holehe.modules.programing.github",
    
    # Real Estate
    "holehe.modules.real_estate.vrbo",
    
    # Shopping
    "holehe.modules.shopping.amazon",
    "holehe.modules.shopping.ebay",
    
    # Software
    "holehe.modules.software.archive",
    "holehe.modules.software.docker",
    "holehe.modules.software.firefox",
    "holehe.modules.software.lastpass",
    "holehe.modules.software.office365",
    
    # Sports
    "holehe.modules.sport.bodybuilding",
    
    # Transport
    "holehe.modules.transport.blablacar"
]

def setup_logging(level: str = "info", log_file: Optional[str] = None) -> None:
    """
    Configure logging for internal debugging.
    """
    logger = logging.getLogger()
    logger.handlers.clear()
    
    log_level = getattr(logging, level.upper(), logging.WARNING)
    logger.setLevel(log_level)
    
    # Use the logging format you preferred
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Add file handler if specified
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except IOError as e:
            print(f"Warning: Could not create log file {log_file}: {e}", file=sys.stderr)

    # KEY FIX: Control the httpx logger to show logs at 'info' and 'debug' levels
    httpx_logger = logging.getLogger("httpx")

    # Besides info and debug, no idea if the others work correctly.
    if level.lower() == "info":
        httpx_logger.setLevel(logging.INFO)
    elif level.lower() == "debug":
        httpx_logger.setLevel(logging.DEBUG)
    elif level.lower() == "warning":
        httpx_logger.setLevel(logging.WARNING)
    elif level.lower() == "error":
        httpx_logger.setLevel(logging.ERROR)
    elif level.lower() == "critical":
        httpx_logger.setLevel(logging.CRITICAL)
    else:
        httpx_logger.setLevel(logging.INFO)


def load_site_modules() -> Dict[str, Any]:
    """Dynamically load all site checking modules."""
    modules = {}
    logger = logging.getLogger(__name__)
    
    for module_path in SITE_MODULES:
        try:
            module = importlib.import_module(module_path)
            site_name = module_path.split('.')[-1]
            check_function = getattr(module, site_name)
            modules[site_name] = check_function
        except (ImportError, AttributeError) as e:
            logger.debug(f"Failed to load module {module_path}: {str(e)}")
    return modules

# Load modules once at startup
SITE_CHECKERS = load_site_modules()

async def check_site(email: str, client: httpx.AsyncClient, site_name: str, 
                     check_function: callable, out: List[Dict[str, Any]]) -> None:
    """
    Check if email is registered on a specific site.
    Errors from the modules are logged at debug level.
    """
    logger = logging.getLogger(__name__)
    # This message is correctly set to 'debug' level
    logger.debug(f"Checking {site_name} for {email}")
    try:
        # The check functions from holehe append results to the 'out' list
        await check_function(email, client, out)
        logger.debug(f"Successfully checked {site_name}")
    except Exception as e:
        # Log the error at debug level, as these are common in the holehe modules
        logger.debug(f"Error checking {site_name}: {str(e)}")


async def check_sites(email: str, client: httpx.AsyncClient, 
                     sites: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Check if email is registered on multiple sites concurrently."""
    out = []
    sites_to_check = sites if sites else list(SITE_CHECKERS.keys())
    
    async with trio.open_nursery() as nursery:
        for site_name in sites_to_check:
            if site_name in SITE_CHECKERS:
                nursery.start_soon(
                    check_site, 
                    email, 
                    client, 
                    site_name, 
                    SITE_CHECKERS[site_name], 
                    out
                )
    
    return out

def read_emails_from_file(file_path: str) -> List[str]:
    """Read email addresses from a file."""
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except IOError as e:
        print(f"Error reading file {file_path}: {str(e)}", file=sys.stderr)
        return []

def write_results_to_file(results: Dict[str, Any], file_path: str) -> None:
    """Write results to a JSON file."""
    try:
        with open(file_path, 'a') as file:
            json.dump(results, file)
            file.write("\n")
    except IOError as e:
        print(f"Error writing to file {file_path}: {str(e)}", file=sys.stderr)

async def process_email(email: str, client: httpx.AsyncClient, 
                       output_file: Optional[str] = None,
                       sites: Optional[List[str]] = None,
                       verbose: bool = False) -> None:
    """
    Process a single email address, check sites, and print/save results.
    """
    sites_to_check = sites if sites else list(SITE_CHECKERS.keys())
    
    print(f"\n[-] Checking email: {email}")
    if verbose:
        print(f"[*] Checking {len(sites_to_check)} sites...")
    
    try:
        data = await check_sites(email, client, sites_to_check)
        found_sites = [] # List to store formatted strings for JSON output

        for results in data:
            if "error" in results and results["error"]:
                continue
            
            if results.get("exists"):
                toprint = ""
                
                if results.get("emailrecovery"):
                    toprint += f" {results['emailrecovery']}"
                
                if results.get("phoneNumber"):
                    toprint += f" - {results['phoneNumber']}"
                
                if results.get("others") and isinstance(results["others"], dict):
                    others = results["others"]
                    if "FullName" in others:
                        toprint += f" - fullname {others['FullName']}"
                    if "Date, time of the creation" in others:
                        toprint += f" - Date, time of the creation {others['Date, time of the creation']}"

                result_string = f"[+] Found: {results['domain']}{toprint}"
                print(result_string)
                found_sites.append(result_string)

        # Print a summary of the results
        if found_sites:
            print(f"\n[---] Summary for {email}: Found {len(found_sites)} accounts [---]")
            for site in found_sites:
                print(f"  - {site}")
        else:
            print(f"\n[---] Summary for {email}: No accounts found [---]")

        if output_file and found_sites:
            results_json = {"email": email, "social": found_sites}
            write_results_to_file(results_json, output_file)
            
    except Exception as e:
        print(f"[!] An unexpected error occurred while processing {email}: {str(e)}", file=sys.stderr)

async def main() -> None:
    """Main function to parse arguments and process emails."""
    parser = argparse.ArgumentParser(
        description="Check if an email is associated with various online accounts."
    )
    parser.add_argument("--email", "-e", help="Email to check.", type=str)
    parser.add_argument("--input", "-i", help="File with emails (one per line).", type=str)
    parser.add_argument("--output", "-o", help="File to save results to (JSON format).", type=str)
    parser.add_argument("--sites", "-s", help="Comma-separated list of sites to check.", type=str)
    parser.add_argument("--list-sites", "-l", action="store_true", help="List all available sites and exit.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show verbose output (number of sites being checked).")
    parser.add_argument("--log", action="store_true", help="Set logging or not.")
    parser.add_argument("--debug", "-d", action="store_true", help="Set debug.")
    
    # Logging options
    parser.add_argument("--log-file", help="Path to log file for internal debugging.", type=str)
    parser.add_argument("--log-level", 
                       choices=["debug", "info", "warning", "error", "critical"],
                       help="Set logging level for console/file output (default: warning).")
    
    
    args = parser.parse_args()
    
    # Probably did this wrong, but if log_level is set, then everything else is ignored.
    # Yes, I know, a little stupidly designed, but I am not a programmer. I do this for free.
    if args.log_level:
        # Setup logging for internal debugging
        setup_logging(
            level=args.log_level,
            log_file=args.log_file
        )
    elif args.log:
        setup_logging(
            level="info",
            log_file=args.log_file
        )
    elif args.debug:
        setup_logging(
            level="debug",
            log_file=args.log_file
        )
    
    if args.list_sites:
        print("Available sites to check:")
        for site in sorted(SITE_CHECKERS.keys()):
            print(f"  - {site}")
        return
    
    sites_to_check = None
    if args.sites:
        sites_to_check = [site.strip() for site in args.sites.split(',')]
        invalid_sites = [site for site in sites_to_check if site not in SITE_CHECKERS]
        if invalid_sites:
            print(f"Error: Invalid sites specified: {', '.join(invalid_sites)}", file=sys.stderr)
            return
    
    emails = []
    
    if args.email:
        emails.append(args.email)
    elif args.input:
        emails = read_emails_from_file(args.input)
        if not emails:
            print("Error: No valid emails found in the input file.", file=sys.stderr)
            return
    else:
        parser.print_help()
        return
    
    # Create HTTP client with reasonable timeout and connection limits
    timeout = httpx.Timeout(10.0, connect=5.0)
    limits = httpx.Limits(max_keepalive_connections=20, max_connections=100)
    
    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
        for email in emails:
            await process_email(email, client, args.output, sites_to_check, args.verbose)

if __name__ == "__main__":
    trio.run(main)
=======

# I hate python
from holehe.modules.social_media.discord import discord
from holehe.modules.social_media.instagram import instagram
from holehe.modules.social_media.twitter import twitter
from holehe.modules.social_media.snapchat import snapchat
from holehe.modules.social_media.bitmoji import bitmoji
from holehe.modules.social_media.crevado import crevado
from holehe.modules.social_media.fanpop import fanpop
from holehe.modules.social_media.imgur import imgur
from holehe.modules.social_media.myspace import myspace
from holehe.modules.social_media.parler import parler
from holehe.modules.social_media.patreon import patreon
from holehe.modules.social_media.pinterest import pinterest
from holehe.modules.social_media.plurk import plurk
from holehe.modules.social_media.strava import strava
from holehe.modules.social_media.taringa import taringa
from holehe.modules.social_media.tellonym import tellonym
from holehe.modules.social_media.tumblr import tumblr
from holehe.modules.social_media.vsco import vsco
from holehe.modules.social_media.wattpad import wattpad
from holehe.modules.social_media.xing import xing

from holehe.modules.cms.gravatar import gravatar
from holehe.modules.cms.atlassian import atlassian
from holehe.modules.cms.wordpress import wordpress
from holehe.modules.cms.voxmedia import voxmedia

from holehe.modules.company.aboutme import aboutme

from holehe.modules.crm.amocrm import amocrm
from holehe.modules.crm.axonaut import axonaut
from holehe.modules.crm.hubspot import hubspot
from holehe.modules.crm.insightly import insightly
from holehe.modules.crm.nimble import nimble
from holehe.modules.crm.nocrm import nocrm
from holehe.modules.crm.nutshell import nutshell
from holehe.modules.crm.pipedrive import pipedrive
from holehe.modules.crm.teamleader import teamleader
from holehe.modules.crm.zoho import zoho

from holehe.modules.crowfunding.buymeacoffee import buymeacoffee

from holehe.modules.jobs.coroflot import coroflot
from holehe.modules.jobs.freelancer import freelancer
from holehe.modules.jobs.seoclerks import seoclerks

from holehe.modules.learning.diigo import diigo
from holehe.modules.learning.quora import quora

from holehe.modules.mails.google import google
from holehe.modules.mails.laposte import laposte
from holehe.modules.mails.protonmail import protonmail
from holehe.modules.mails.yahoo import yahoo

from holehe.modules.medias.ello import ello
from holehe.modules.medias.flickr import flickr
from holehe.modules.medias.komoot import komoot
from holehe.modules.medias.rambler import rambler
from holehe.modules.medias.sporcle import sporcle

from holehe.modules.medical.caringbridge import caringbridge
from holehe.modules.medical.sevencups import sevencups

from holehe.modules.music.soundcloud import soundcloud
from holehe.modules.music.spotify import spotify

from holehe.modules.osint.rocketreach import rocketreach

from holehe.modules.payment.venmo import venmo

from holehe.modules.porn.pornhub import pornhub
from holehe.modules.porn.redtube import redtube
from holehe.modules.porn.xnxx import xnxx
from holehe.modules.porn.xvideos import xvideos

from holehe.modules.productivity.evernote import evernote
from holehe.modules.productivity.anydo import anydo

from holehe.modules.products.eventbrite import eventbrite
from holehe.modules.products.nike import nike

from holehe.modules.programing.github import github

from holehe.modules.real_estate.vrbo import vrbo

from holehe.modules.shopping.amazon import amazon
from holehe.modules.shopping.ebay import ebay

from holehe.modules.software.archive import archive
from holehe.modules.software.docker import docker
from holehe.modules.software.firefox import firefox
from holehe.modules.software.lastpass import lastpass
from holehe.modules.software.office365 import office365

from holehe.modules.sport.bodybuilding import bodybuilding
from holehe.modules.transport.blablacar import blablacar

# This "module" library is designed like shit and I am not ready to try to make this code better anytime soon.

async def chk_sites(email, client, out):

    data = dict()
    
    try:
        await blablacar(email, client, out)
    except Exception:
        pass

    try:
        await bodybuilding(email, client, out)
    except Exception:
        pass

    try:
        await office365(email, client, out)
    except Exception:
        pass

    try:
        await lastpass(email, client, out)
    except Exception:
        pass

    try:
        await firefox(email, client, out)
    except Exception:
        pass

    try:
        await docker(email, client, out)
    except Exception:
        pass

    try:
        await archive(email, client, out)
    except Exception:
        pass

    try:
        await ebay(email, client, out)
    except Exception:
        pass
    
    try:
        await amazon(email, client, out)
    except Exception:
        pass
    
    try:
        await vrbo(email, client, out)
    except Exception:
        pass

    try:
        await github(email, client, out)
    except Exception:
        pass

    try:
        await nike(email, client, out)
    except Exception:
        pass

    try:
        await eventbrite(email, client, out)
    except Exception:
        pass
    
    try:
        await anydo(email, client, out)
    except Exception:
        pass
    try:
        await evernote(email, client, out)
    except Exception:
        pass

    try:
        await xvideos(email, client, out)
    except Exception:
        pass
    
    try:
        await xnxx(email, client, out)
    except Exception:
        pass

    try:
        await redtube(email, client, out)
    except Exception:
        pass

    try:
        await pornhub(email, client, out)
    except Exception:
        pass

    try:
        await venmo(email, client, out)
    except Exception:
        pass

    try:
        await rocketreach(email, client, out)
    except Exception:
        pass

    try:
        await spotify(email, client, out)
    except Exception:
        pass

    try:
        await soundcloud(email, client, out)
    except Exception:
        pass

    try:
        await sevencups(email, client, out)
    except Exception:
        pass

    try:
        await caringbridge(email, client, out)
    except Exception:
        pass

    try:
        await sporcle(email, client, out)
    except Exception:
        pass

    try:
        await rambler(email, client, out)
    except Exception:
        pass

    try:
        await komoot(email, client, out)
    except Exception:
        pass

    try:
        await flickr(email, client, out)
    except Exception:
        pass

    try:
        await ello(email, client, out)
    except Exception:
        pass

    try:
        await yahoo(email, client, out)
    except Exception:
        pass

    try:
        await protonmail(email, client, out)
    except Exception:
        pass

    try:
        await laposte(email, client, out)
    except Exception:
        pass

    try:
        await google(email, client, out)
    except Exception:
        pass

    try:
        await quora(email, client, out)
    except Exception:
        pass

    try:
        await diigo(email, client, out)
    except Exception:
        pass

    try:
        await seoclerks(email, client, out)
    except Exception:
        pass

    try:
        await freelancer(email, client, out)
    except Exception:
        pass

    try:
        await coroflot(email, client, out)
    except Exception:
        pass

    try:
        await buymeacoffee(email, client, out)
    except Exception:
        pass

    try:
        await zoho(email, client, out)
    except Exception:
        pass

    try:
        await teamleader(email, client, out)
    except Exception:
        pass

    try:
        await pipedrive(email, client, out)
    except Exception:
        pass
    
    try:
        await nutshell(email, client, out)
    except Exception:
        pass
    
    try:
        await nocrm(email, client, out)
    except Exception:
        pass

    try:
        await nimble(email, client, out)
    except Exception:
        pass


    try:
        await insightly(email, client, out)
    except Exception:
        pass

    try:
        await hubspot(email, client, out)
    except Exception:
        pass

    try:
        await axonaut(email, client, out)
    except Exception:
        pass

    try:
        await amocrm(email, client, out)
    except Exception:
        pass

    try:
        await aboutme(email, client, out)
    except Exception:
        pass

    try:
        await xin(email, client, out)
    except Exception:
        pass


    try:
        await wattpad(email, client, out)
    except Exception:
        pass


    try:
        await vsco(email, client, out)
    except Exception:
        pass


    try:
        await tumblr(email, client, out)
    except Exception:
        pass

    try:
        await tellonym(email, client, out)
    except Exception:
        pass

    try:
        await taringa(email, client, out)
    except Exception:
        pass

    try:
        await strava(email, client, out)
    except Exception:
        pass

    try:
        await plurk(email, client, out)
    except Exception:
        pass

    try:
        await pinterest(email, client, out)
    except Exception:
        pass

    try:
        await patreon(email, client, out)
    except Exception:
        pass

    try:
        await parler(email, client, out)
    except Exception:
        pass
   
    try:
        await myspace(email, client, out)
    except Exception:
        pass
  
    try:
        await imgur(email, client, out)
    except Exception:
        pass

    try:
        await fanpop(email, client, out)
    except Exception:
        pass    
    try:
        await crevado(email, client, out)
    except Exception:
        pass

    try:
        await bitmoji(email, client, out)
    except Exception:
        pass

    try:
        await atlassian(email, client, out)
    except Exception:
        pass

    try:
        await wordpress(email, client, out)
    except Exception:
        pass
    
    try:
        await voxmedia(email, client, out)
    except Exception:
        pass

    try:
        await discord(email, client, out)
    except Exception:
        pass

    try:
        await gravatar(email, client, out)
    except Exception:
        pass
    
    try:
        await instagram(email, client, out)
    except Exception:
        pass

    try:
        await twitter(email, client, out)
    except Exception:
        pass

    try:
        await snapchat(email, client, out)
    except Exception:
        pass
    
    data = out.copy()
    out.clear() # I hate python3.

    return data

def read_file(file):
    try:
        # Read file using readlines
        fd = open(file, 'r')
        lines = fd.readlines()
 
        return lines
    except Exception as error:
        print("Error at read_file: {}".format(error))

def write_file(data, file):
    fd = open(file, "a")

    # This is dumb.
    fd.writelines(line + '\n' for line in data)
    fd.close()

def write_email(data, file):
    fd = open(file, "a")

    # This is dumb.
    fd.writelines(data + '\n')
    fd.close()
        
async def main():
    chk_emails = list()
    final_data = list()
    
    data = dict()

    out = []

    client = httpx.AsyncClient()

    parser=argparse.ArgumentParser(description="Simple python3 program to check if an email is associated with any of the import online account modules.")
    parser.add_argument("--email", "-e", help="Email to check.", type=str)
    parser.add_argument("--input", "-i", help="File with emails one on each line.", type=str)
    parser.add_argument("--output", "-o", help="Specify a file to save results to.", type=str)
    args=parser.parse_args()

    if args.email is not None:
        chk_emails.append(args.email)
    elif args.input is not None:
        emails = read_file(args.input)
        
        for email in emails:
            chk_emails.append(email.strip())
    else:
        parser.print_help()

    if chk_emails is not None:
        for email in chk_emails:
            final_data.clear()
            data.clear()

            try:
                print("Checking email: " + email)
                data = await chk_sites(email, client, out)

                # This I did take from the example code here: https://github.com/megadose/holehe/blob/master/holehe/core.py
                # the function I borrowed is print_results() starting at line 106.
                # I just added the json part.
                for results in data:
                    if "error" in results.keys() and results["error"]:
                        toprint = ""
                        if results["others"] is not None and "Message" in str(results["others"].keys()):
                            toprint = " Error message: " + results["others"]["errorMessage"]
                        print(" " + results["domain"])
                    elif results["exists"] == True:
                        toprint = ""
                        if results["emailrecovery"] is not None:
                            toprint += " " + results["emailrecovery"]
                        if results["phoneNumber"] is not None:
                            toprint += " - " + results["phoneNumber"]
                        if results["others"] is not None and "FullName" in str(results["others"].keys()):
                            toprint += " - fullname " + results["others"]["FullName"]
                        if results["others"] is not None and "Date, time of the creation" in str(results["others"].keys()):
                            toprint += " - Date, time of the creation " + results["others"]["Date, time of the creation"]

                        print("Found: " + results["domain"] + toprint)

                        final_data.append(results["domain"] + toprint)

                if final_data is not None and args.output is not None:
                    data = {"email": email, "social": final_data}
                    
                    print(json.dumps(data))
                    
                    with open(args.output, "a") as fd:
                        json.dump(data, fd)
                        fd.write("\n")
                    #write_email(email, args.output)
                    #write_file(final_data, args.output)

            except Exception:
                pass

   
    await client.aclose()

trio.run(main)
>>>>>>> 63af29e3f66952549618736a5574588301c05b28
