#!/usr/bin/env python3

import click
import os
import sqlite3
import CreatureReport
import auditing
import config


@click.group()
def cli():
	"""Utilities for Nature App"""
	pass

@cli.group()
def settings():
	"""Show Birdbrain's current config"""
	click.echo('\n\n\nBirdbrain config\n\n')

@cli.command()
def install():
	"""Install APK on device"""
	# This could trigger some tests before allowing us to safely
	# allow APK installation. For example, to stop us if the OBB
	# configuration is not right
	
	pass

@cli.command()
def status():
	"""Reports OBB situation."""
    
	#TODO: This should also launch the audit.

	click.echo(f'\n\n\n\nBirdbrain status')
	click.echo(f'----------------')

	click.echo('\nApp version:')
	cmd = f'grep "versionCode" {config.PATH_APP}/app/build.gradle'
	os.system(cmd)

	click.echo('\nSet up for expansion pack version:')
	cmd = f'grep -A 1 "obbVersion" {config.PATH_APP}/app/build.gradle'
	os.system(cmd)

	click.echo('\nOn phone right now:')
	cmd = f'adb shell ls {config.OBB_DESTINATION_DIR}'
	os.system(cmd)

	click.echo('\n\n')

@cli.command()
@click.option("--original", default=False, help="Use original version")
def pack(original):
	"""Install OBB expansion pack on Android device"""
	if (original == True):
		destination_dir = config.OBB_DESTINATION_DIR_ORIGINAL
		version = 37
		app_package = "com.gorenfeld.natureapp"
	else:
		destination_dir = config.OBB_DESTINATION_DIR    
		version = config.OBB_VERSION
		app_package = config.PACKAGE

	filename = f'main.{version}.{app_package}.obb'
	destination_path = f'{destination_dir}/{filename}'
	cmd = f'adb mkdir {destination_dir}'
	os.system(cmd)
	cmd = f'adb push {config.OBB_SOURCE_DIR}/{filename} {destination_path}'
	click.echo(cmd)
	os.system(cmd)

@cli.command()
def unpack():
    """Remove OBB expansion pack from Android device"""

@cli.command()
def optimise():
    """Optimise images."""
	   
@cli.command()
def boot():
    """Run app after installing OBB expansion pack"""
    pass

@cli.command()
def audit():
	"""Check for missing images and songs"""

	auditing.roll_call()
	auditing.songs(CreatureReport)	

@cli.command()
def missing():
	"""List missing plates and stage originals in special dir for conversion"""

	original_species_images = os.listdir(f'{ORIGINAL_SPECIES_IMAGES_PATH}')
	our_species_images = os.listdir(f'{OBB_SOURCE_DIR}/images/species')

	click.echo(f'Found {len(original_species_images)} family image files')    
	click.echo(f'Found {len(our_species_images)} species images staged to be put into expansion pack')

	i = 0

	need_conversion = []

	for original in original_species_images:
		name = original[:-3] + "jpg"
	if name not in our_species_images:
			i = i + 1
			need_conversion.append(original)
			click.echo(f'{i}. {name}')
		  
	click.echo(len(need_conversion))


@cli.command()
def forge():
	"""Build new expansion pack from assets"""

	# zip -r0 zipfilename.zip files-to-zip

	obb_source_dir = config.PATH_OBB_SOURCE
	obb_filename = config.OBB_FILENAME
	obb_creation_path = config.PATH_OBB_CREATION

	cmd = f'cd {obb_source_dir} && zip -r0 {obb_filename} ./ -x "*.obb"'
	click.echo(cmd)
	os.system(cmd)

	click.echo('Resulting in this OBB:')
	size_cmd = f'ls -lh {obb_creation_path}'
	os.system(size_cmd)


@cli.command()
def plumagenames():
	"""Fit plumage filenames to CreatureReport entries"""
	pass

@cli.command()
def species():
	"""Prepare species images"""
	cmd = 'mogrify -verbose -format jpg -background white -alpha remove -flatten -alpha off -define jpeg:extent=400kb -path /Users/johngorenfeld/Dropbox/natureapp/assets/expansion/images/species *.png'
	os.system(cmd)


@cli.command()
@click.argument('id')
def ref(id):
	"""Get a CreatureReport object's reference from its ID"""
	if id is None:
		print("Must provide valid CreatureReport entity ID.")
		return

	found_ref = CreatureReport.lookup_ref(id)
	if ref is None:
		click.echo('No ref found in CreatureReport database.')
		return
	click.echo(found_ref)

@cli.command()
@click.argument('ref')
def id(ref):
	"""Get a CreatureReport object's ID from its reference"""
	if ref is None:
		print("Must provide valid CreatureReport entity reference.")
		return

	query_key=f'SELECT entity_id FROM CreatureReport_entities WHERE entity_reference={ref}'
	conn = sqlite3.connect(CreatureReport_DB_PATH)
	c = conn.cursor()

	for row in c.execute(query_key):
		id = row[0]

	click.echo(id)

@cli.command()
@click.argument('ref')
def name(ref):
	"""Compose ideal NatureApp filename"""

	# Future version of this can support other categories but right
	# now this is strictly for songs.

	# Songs
	clean_ref = ref.replace(".wav", "")

	new_name = helpers.name_song(clean_ref)
	click.echo(new_name)

@cli.command()
@click.argument('name')
def modernname(name):
	"""Determine proper name for Legacy file"""

	# Future version of this can support other categories but right
	# now this is strictly for songs.

	# TODO: Deduce file category from name
	# TODO: Or pass in a nested enum argument

	# Songs

	id = name.split('.')[0]
	ref = CreatureReport.lookup_ref(id)
	if ref is None:
		click.echo(f'No CreatureReport reference found for id {id}.')
		return

	clean_ref = ref.replace(".wav", "")

	song_name = helpers.name_song(clean_ref)
	click.echo(song_name)

@cli.command()
@click.argument('id')
def songs(id):
	"""Get array of song IDs that belong to a particular animal"""
	return CreatureReport.get_song_IDs_for_species_ID(id)

if __name__ == '__main__':
	CreatureReport = CreatureReport.CreatureReportDatabase(config.CreatureReport_DB_PATH)

	cli()
