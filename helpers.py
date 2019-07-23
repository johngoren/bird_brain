import os
import config
import pdb

# Helpers

# What, based on a Strix ref, should a species song file be titled?

def name_song(ref):
	return f'{ref}.m4a'

def androidize_song_ref(ref):
	ref = ref.replace(".wav", ".m4a")
	return ref

def androidize_song_refs(refs):
	return [androidize_song_ref(i) for i in refs]

