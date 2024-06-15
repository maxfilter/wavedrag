#!/usr/bin/env python3
# (C) 2018--2024 Ed Bueler

# The purpose of this code is to generate a flow-line domain,
# suitable for meshing, on which we can solve the Stokes equations.
# See README.md and flow.py for usage in the Stokes context.
# Basic usage:
#   $ ./domain.py glacier.geo
#   $ gmsh -2 glacier.geo
# This generates glacier.msh.  You can use gmsh to inspect the mesh,
# or you can load it into python using firedrake.  For example:
#   $ source firedrake/bin/activate
#   (firedrake) $ ipython3
#   In [1]: from firedrake import *
#   In [2]: Mesh('glacier.msh')

bdryids = {'outflow' : 41,
           'top'     : 42,
           'inflow'  : 43,
           'base'    : 44}

def writegeo(geo_filename, param_name, param_val, outputfilename):

    #write parameters into the geofile
    with open(geo_filename, 'r') as geoi:

        lines = geoi.readlines()
        
        with open(outputfilename,'w') as geoo:

            for i in range(len(param_name)):
                geoo.write(param_name[i] + ' = ' + str(param_val[i]) + ';')
            for l in lines:
                geoo.write(l)    

def processopts():
    import argparse
    parser = argparse.ArgumentParser(description=
    '''Generate .geo geometry-description file, suitable for meshing by Gmsh,
    for the outline of a glacier flow domain with sinusoidal waves.  Also
    generates slab-on-slope geometry with -wamp 0, where -wfreq value will be ignored.
    ''')
    parser.add_argument('-wamp', type=float, default=10.0, metavar='X', 
                        help='amplitude of sine wave (default=10 m)')
    parser.add_argument('-wfreq', type=float, default=10.0, metavar='X',
                        help='frequency of sine wave (default=10 m)')
    parser.add_argument('-H', type=float, default=400.0, metavar='X',
                        help='thickness of ice (default=400 m)')
    parser.add_argument('-L', type=float, default=3000.0, metavar='X',
                        help='flow line length (default=3000 m)')
    parser.add_argument('-i', metavar='FILE.geo', default='glacier.geo',                        help='baseline geo file to modify (ends in .geo; default=glacier.geo)')
    parser.add_argument('-o', metavar='FILE.geo', default='glacier_modified.geo', help='if specified, the original file will not be modified, but an output will be produced instead')
    return parser.parse_args()

if __name__ == "__main__":
    from datetime import datetime
    import sys, platform, subprocess

    args = processopts()
    commandline = " ".join(sys.argv[:])  # for save in comment in generated .geo
    if len(sys.argv)!=13:
        print('please use this file by replacing {x} with appropriate values: ./domain.py -o {output_filename.geo} -i {provided_geo_file.geo} -wamp {amplitude of the wave} -wfreq {frequency of the wave} -L {total length of the slab} -H {thickness of the slab}')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    outputfilename = args.o
    geofilename = args.i
    if len(outputfilename)==0:
        print('writing geometry to the input file -i %s' % geofilename)
    else:
        print('writing geometry to another output file -o %s' % outputfilename)
    # write the rest of the .geo file
    param_name = ['A','F','X','H']
    param_val = [args.wamp,args.wfreq,args.L,args.H]
    writegeo(args.i,param_name,param_val,outputfilename)
