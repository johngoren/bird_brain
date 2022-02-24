import os
import files
import config
import click
import helpers
import pdb



#  Report on number of files, and launch other audits

def roll_call():
	path_expansion_assets = config.PATH_OBB_SOURCE
	path_songs = config.PATH_SONGS

	path_family_images = config.PATH_FAMILY
	path_species_images = config.PATH_SPECIES_IMAGES_FULL
	path_thumbs = config.PATH_SPECIES_IMAGES_THUMBNAIL

	species_images = os.listdir(path_species_images)

	num_family_images = 47
	num_species_images = config.NUM_SPECIES_IMAGES
	num_thumbs = num_species_images
	num_songs = config.NUM_SONGS

	plumage_images = os.listdir(f'{path_expansion_assets}/images/plumages')
	map_images = os.listdir(f'{path_expansion_assets}/images/maps')
	family_images = os.listdir(f'{path_family_images}')
	songs = os.listdir(path_songs)
	thumbs = os.listdir(path_thumbs)

	audit_echo("family images", len(family_images), num_family_images)
	audit_echo("species images", len(species_images), num_species_images )
	audit_echo("thumbs", len(thumbs), num_thumbs)
	audit_echo("plumage image files", len(plumage_images), None)
	audit_echo("songs", len(songs), num_songs)

# Audit bird songs

def songs(CreatureReport):
	not_found = 0

	song_files_list = files.get_song_files_from_disk()
	species_id_list = CreatureReport.get_species_id_list()

	for id in species_id_list:
		songs_for_this_species = CreatureReport.get_song_refs_for_species(id)
		android_filenames = helpers.androidize_song_refs(songs_for_this_species)
		missing = check_my_songs_are_found(android_filenames, song_files_list)
		if missing > 0:
			not_found = not_found + missing

	if not_found > 0:
		click.secho(f'Missing {not_found} songs', fg='red')
	else:
		click.secho("All song files found", fg="green")

	not_in_db = 0
	song_refs_in_CreatureReport = CreatureReport.get_all_song_refs()

	for file in song_files_list:
		absent = check_file_also_in_DB(file, song_refs_in_CreatureReport)
		if absent > 0:
			not_in_db = not_in_db + absent

	if not_in_db > 0:		
		click.secho(f'{not_in_db} possibly surplus files were found that do not have direct CreatureReport counterparts', fg='yellow')
	

# Check if a single bird's songs exist as files

def check_my_songs_are_found(songs_for_this_species, master_song_list):
	not_found = 0

	for song in songs_for_this_species:
		if song not in master_song_list:
			click.secho(f'{song} audio file not found', fg='red')
			not_found = not_found + 1

	return not_found


# Check that a song appears in the DB

def check_file_also_in_DB(filename, master_CreatureReport_song_list):
	possible_refs = helpers.CreatureReportify_song_filename(filename)
	for ref in possible_refs:
		if ref in master_CreatureReport_song_list:
			return 0 # We found it. No absence
	
	click.echo(f'{possible_refs[2]} is on disk but not in CreatureReport')
	return 1 # Tally this one as absent

	
def audit_echo(category, found, desired):

	text = f'Found {found} {category}'

	if desired is None:
		text = f'   {text}'
		click.echo(text)
		return
	if found == desired:
		checkmark = '   '
		text = f'{checkmark}{text}'
		click.secho(text, fg='green')
	else:
		text = ' x ' + text
		text = text + f' (expected {desired})'
		click.secho(text, fg='yellow')
	
	


