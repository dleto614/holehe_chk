import trio
import httpx
import json
import argparse

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