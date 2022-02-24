import os
import config
import pdb

# Helpers

# What, based on a CreatureReport ref, should a species song file be titled?

def name_song(ref):
	return f'{ref}.m4a'

def androidize_song_ref(ref):
	# TODO: Account for names without extensions
	# TODO: Also make sure this is handled in-app

	ref = ref.replace(".wav", ".m4a").replace(".mp3", ".m4a")
	if ".m4a" not in ref:
		ref = ref + ".m4a"

	return ref

# A list of song refs transformed from .wav or .mp3 to .m4a

def androidize_song_refs(refs):
	return [androidize_song_ref(i) for i in refs]

def CreatureReportify_song_filename(name):
	name1 = name.replace(".m4a", ".wav")
	name2 = name.replace(".m4a", ".mp3")
	name3 = name.replace(".m4a", "")
	return [name1, name2, name3]

