#!/usr/bin/env python
# File created on 13 Sep 2012
#from __future__ import division

__author__ = "John Chase"
__copyright__ = "Copyright 2011, The QIIME project"
__credits__ = ["John Chase"]
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "John Chase"
__email__ = "jc33@nau.edu"
__status__ = "Development"
 
from personal_microbiome.util import create_personal_results
from qiime.util import parse_command_line_parameters, make_option
import os
from os.path import exists, join
from os import makedirs 

script_info = {}
script_info['brief_description'] = """Generate distinct 3d plots for unique individuals based on the metadata mapping file."""
script_info['script_description'] = """This script generates a prefs file which assigns a unique color to the individual and then generates a 3d plot based on that prefs file"""
script_info['script_usage'] = [("""Basic usage with output directory""", """The distance matrix and mapping files are required. if no output file path is specified one will be created in the working directory. """, """%prog -i distance_matrix.txt -m mapping_file.txt -o out/""")]
script_info['output_description'] = "A directory containing all of the 3d plots for each individual"
script_info['required_options'] = [
    make_option('-m', '--mapping_fp', type='existing_filepath', 
        help='Metadata mapping file filepath'),
    make_option('-i', '--coord_fname',
        help='Input principal coordinates filepath (i.e.,'
        ' resulting file from principal_coordinates.py). Alternatively,'
        ' a directory containing multiple principal coordinates files for'
        ' jackknifed PCoA results.',
        type='existing_path'),
    make_option('-c', '--collated_dir',
        help='Input collated directory filepath (i.e.,'
        ' resulting file from collate_alpha.py)',
        type='existing_path'),
    make_option('-o', '--output_dir',
        help="Output directory. One will be created if it doesn't exist.",
        type='new_dirpath'),
    make_option('-p', '--prefs_fp',
        help='Input prefs filepath, this is user generated (i.e.,'
        'not currently created from any qiime function)',
        type='existing_path')
]

script_info['optional_options'] = [
   make_option('-n','--personal_id_column',
        default='PersonalID', type='string',
        help='Name of the column in the header that denotes the individual '
        'of interest, default is PersonalID.'),
   make_option('-l','--personal_ids',
        default=None, type='string',
        help='A comma seperated list of individual ids '
        'the default will create a list of all of the individuals '
        'in the mapping file.'),
   make_option('-t','--column_title',
        default=None, type='string',
        help='Name of the column.'
        'A new column will be created to indicate '
        'whether a sample is from the specified individual '
        'or from a differeent individual. This option defines '
        'the name of that column. Default is "Self" '
        'This change requires that the prefs file is modified as well '),
   make_option('-r','--individual_titles',
        default=None, type='string',
        help='Comma seperated values, i.e(Self,Other). '
        'The "self" title should be listed first. '
        'The default is "Self" '
        'if the sample is from the individual of interest ' 
        'and "Other" if the sample is not from the person '
        'of interest. Currently this requires modifying '
        'the prefs file to match the indicated titles. ')
        ]   

script_info['version'] = __version__



def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    mapping_file = opts.mapping_fp
    distance_matrix = opts.coord_fname
    collated_dir = opts.collated_dir
    output_dir = opts.output_dir
    prefs = opts.prefs_fp
    personal_id_column = opts.personal_id_column
    personal_ids = opts.personal_ids
    column_title = opts.column_title
    individual_titles = opts.individual_titles
    
    if exists(output_dir):
        # don't overwrite existing output directory - make the user provide a different name or 
        # move/delete the existing directory since it may have taken a while to create.
        raise ValueError, "Output directory (%s) already exists. Won't overwrite." % output_dir

    create_personal_results(mapping_file, 
                            distance_matrix, 
                            collated_dir, 
                            output_dir, 
                            prefs, 
                            personal_id_column, 
                            personal_ids, 
                            column_title, 
                            individual_titles)
    
if __name__ == "__main__":
    main()