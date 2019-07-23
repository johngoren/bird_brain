import os
import strix


# Does this file exist in expansion pack asset loading directory?
def roll_call():
	path_app_assets = config.PATH_APP_ASSETS
	path_expansion_assets = config.PATH_EXPANSION_ASSETS
	path_songs = config.PATH_SONGS

	path_family_images = os.listdir(f'{path_app_assets}/images/family')
	path_species_images = f'{path_expansion_assets}/images/species'

	species_images = os.listdir(species_path) 
	click.echo(species_path)

	plumage_images = os.listdir(f'{path_expansion_assets}/images/plumages')
	map_images = os.listdir(f'{path_expansion_assets}/images/maps')
	songs = os.listdir{f'{path_songs}'}

	click.echo(f'Found {len(family_images)} family image files')    
	click.echo(f'Found {len(species_images)} species image files')
	click.echo(f'Found {len(plumage_images)} plumage image files')
	click.echo(f'Found {len(songs)} songs')

	if len(species_images) != NUM_SPECIES_IMAGES:
		missing = NUM_SPECIES_IMAGES - len(species_images)
		click.echo(f'{missing} species images may be missing out of a hoped-for {NUM_SPECIES_IMAGES}.')


def songs(songs_list):
    # Loop through all species refs
    # Check if refs are found in songs file list.
    # return    

def missing():
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



