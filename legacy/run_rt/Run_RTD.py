#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      jnolting
#
# Created:     28/06/2013
# Copyright:   (c) jnolting 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os, sys, shutil, json, argparse, stat

def copytree(src, dst, symlinks = False, ignore = None):
  if not os.path.exists(dst):
    os.makedirs(dst)
    shutil.copystat(src, dst)
  lst = os.listdir(src)
  if ignore:
    excl = ignore(src, lst)
    lst = [x for x in lst if x not in excl]
  for item in lst:
    s = os.path.join(src, item)
    d = os.path.join(dst, item)
    if symlinks and os.path.islink(s):
      if os.path.lexists(d):
        os.remove(d)
      os.symlink(os.readlink(s), d)
      try:
        st = os.lstat(s)
        mode = stat.S_IMODE(st.st_mode)
        os.lchmod(d, mode)
      except:
        pass # lchmod not available
    elif os.path.isdir(s):
      copytree(s, d, symlinks, ignore)
    else:
      shutil.copy2(s, d)

def removeShpfile(inFile):
    dirOfInFile = os.path.dirname(inFile)
    locFiles1 = set(os.listdir(dirOfInFile))
    for ff in locFiles1:
        if ff.find(os.path.basename(os.path.splitext(inFile)[0]) + os.path.splitext(ff)[1]) != -1:
            print "removing " + os.path.splitext(inFile)[0] + os.path.splitext(ff)[1]
            os.remove(os.path.splitext(inFile)[0] + os.path.splitext(ff)[1])

    return

def renameShpfile(src, dst):
    dirOfInFile = os.path.dirname(src)
    locFiles1 = set(os.listdir(dirOfInFile))
    for ff in locFiles1:
        if ff.find(os.path.basename(os.path.splitext(src)[0]) + os.path.splitext(ff)[1]) != -1:
            print "renaming " + os.path.splitext(src)[0] + os.path.splitext(ff)[1] + " to " + os.path.splitext(dst)[0] + os.path.splitext(ff)[1]
            os.rename(os.path.splitext(src)[0] + os.path.splitext(ff)[1], os.path.splitext(dst)[0] + os.path.splitext(ff)[1])

    return

def saveShpfile(inFile, changeName):

    dirOfInFile = os.path.dirname(inFile)
    locFiles = set(os.listdir(dirOfInFile))
    remFiles = []
    for ff1 in locFiles:
        if ff1.find(os.path.basename(os.path.splitext(inFile)[0]) + changeName + os.path.splitext(ff1)[1]) != -1:
            remFiles.insert(0, ff1)

    for idx in range(0, len(remFiles)):
        print "removing " + remFiles[idx]
        locFiles.remove(remFiles[idx])

    for ff in locFiles:
        if ff.find(os.path.basename(os.path.splitext(inFile)[0])) != -1:
            if os.path.exists(os.path.join(dirOfInFile, os.path.splitext(ff)[0] + changeName + os.path.splitext(ff)[1])):
                print "removing " + os.path.join(dirOfInFile, os.path.splitext(ff)[0] + changeName + os.path.splitext(ff)[1])
                os.remove(os.path.join(dirOfInFile, os.path.splitext(ff)[0] + changeName + os.path.splitext(ff)[1]))
            print "copy file " + os.path.join(dirOfInFile, ff) + " to " + os.path.join(dirOfInFile, os.path.splitext(ff)[0] + changeName + os.path.splitext(ff)[1])
            shutil.copyfile(os.path.join(dirOfInFile, ff), os.path.join(dirOfInFile, os.path.splitext(ff)[0] + changeName + os.path.splitext(ff)[1]))

    return

def main():

    # check if there was a json file location passed as an argument
    arg_parser = argparse.ArgumentParser(description='This python application requires the location of a json RT parameter file')
    arg_parser.add_argument("--f", action='store', dest='parm_file',
                            help="should be relative path for gbd (can be full path outside of gbd)")
    arg_parser.add_argument("--w", action='store', dest='work_dir',
                            help="needed for status location. if not given the input file directory will be used.")
    
    args = arg_parser.parse_args()
    if(args.work_dir is not None):
        wdir = args.work_dir
    else:
        wdir = os.path.join('/mnt','work')

    status_path = os.path.join(wdir,'status.json')

    if(args.parm_file is None):
        if(os.path.exists(wdir)):      
            if(os.path.exists(status_path)):
               os.remove(status_path)
            with open(status_path,'wb') as status_json_file:
                json_string = '{"status":"failed","reason":"No parm file"}'
                json.dump(json.loads(json_string), status_json_file)
            return
        else:
            print 'No parm file'
            return
    
    parm_json_file = open(args.parm_file,'r')
    parsed_parms = json.load(parm_json_file)
    if(not parsed_parms.has_key('filename')):
        if(os.path.exists(wdir)):      
            if(os.path.exists(status_path)):
               os.remove(status_path)
            with open(status_path,'wb') as status_json_file:
                json_string = '{"status":"failed","reason":"No filename parm"}'
                json.dump(json.loads(json_string), status_json_file)
            return
        else:
            print 'no filename parm'
            return 

    filename = parsed_parms['filename']
    if filename == 'False':
        filename = ''
    gbd_input_path = os.path.join(os.path.join(wdir,'input'), 'data')
    input_dir = gbd_input_path
    full_filename = os.path.join(gbd_input_path, filename)
    if(os.path.isfile(filename)):
        full_filename = filename
        input_dir = os.path.dirname(filename)

    files = []
    if(not os.path.isfile(full_filename)):
        if(os.path.isdir(input_dir)):
            #find all of the files
            testfiles = os.listdir(input_dir)
            for fi in testfiles:
                if os.path.isfile(os.path.join(input_dir,fi)):
                    ffgd = os.path.splitext(fi)
                    if os.path.splitext(fi)[1] == '.tif' or os.path.splitext(fi)[1] == '.TIF':
                        files.append(os.path.join(input_dir,fi))
  
    else:
        files.append(full_filename)

    if files.count is 0:
        if(os.path.isfile(status_path)):
            os.remove(status_path)
        with open(status_path,'wb') as status_json_file:
            json_string = '{"status" : "failed", "reason" : "Input file does not exist"}'
            json.dump(json.loads(json_string), status_json_file)
        print 'No input file ' + full_filename
        return

    if(not parsed_parms.has_key('inputshpname')):
        if(os.path.isdir(wdir)):      
            if(os.path.isfile(status_path)):
               os.remove(status_path)
            with open(status_path,'wb') as status_json_file:
                json_string = '{"status":"failed","reason":"No shapefile to update or make new (need a name even if not exists)"}'
                json.dump(json.loads(json_string), status_json_file)
            return
        else:
            print 'no shapefilename parm'
            return

    inputshpname = parsed_parms['inputshpname']
    full_inputshpname = os.path.join(gbd_input_path, inputshpname)
    if(not os.path.isdir(gbd_input_path)):
       full_inputshpname = inputshpname
            
    if(not os.path.isdir(wdir)):
        wdir = input_dir
        status_path = os.path.join(wdir,'status.json')

    #make status file
    status_json_file = open(status_path,'wb')
    status_string = '{"status":"failed","reason":"did not finish run"}'
    json.dump(json.loads(status_string), status_json_file)  
    status_json_file.close()  

    gbd_base_outdir = os.path.join(wdir,'output')
    if(parsed_parms.has_key('outputdir')):
        outdir = parsed_parms['outputdir']
    else:
        outdir = os.path.join(gbd_base_outdir, 'out')

    transfer_support = False
    if(os.path.isdir(gbd_base_outdir)):
        transfer_support = True
    
    vupt_exe = "/dglabs/bin/dglabs/GeoTracker_Drivers/Release_develop_x64/VUPT_Driver_Release_develop_x64"
    if(parsed_parms.has_key('vuptexecutable')):
        vupt_exe = parsed_parms['vuptexecutable']
    command = vupt_exe
    command += " -sf " + full_inputshpname

    if(parsed_parms.has_key('featuretype')):
        ftype = parsed_parms['featuretype']
    else:
        print 'Updating with Dirt Urban'
        featureType = 'd'

    if((ftype == u'Dirt Urban') or (ftype == u'Dirt Urban') or (ftype == u'Dirt Urban')):
        featureType = 'd'
    elif((ftype == u'Trails') or (ftype == u'trails')):
        featureType = 't'
    elif((ftype == u'Suburban') or (ftype == u'suburban')):
        featureType = 's'
    elif((ftype == u'Rivers') or (ftype == u'rivers')):
        featureType = 'r'
    elif((ftype == u'Oil') or (ftype == u'oil fields') or (ftype == u'Oil Fields')):
        featureType = 'o'
    elif((ftype == u'Boundaries') or (ftype == u'boundaries')):
        featureType = 'b'
    else:
        print 'Updating with Dirt Urban'
        featureType = 'd'
    
    command += " -ft " + featureType

    nthreads = '8'
    if(parsed_parms.has_key('numthreads')):
        nthreads = parsed_parms['numthreads']
    command += " -nt " + nthreads
    
    if(parsed_parms.has_key('outputshpfilename')):
        out_shp_file = parsed_parms['outputshpfilename']
        out_shp_file_full = os.path.join(outdir, out_shp_file) 
        if(not os.path.exists(outdir)):
            out_shp_file_full = out_shp_file    
    else:
        tshpname = os.path.splitext(os.path.basename(full_inputshpname))[0]
        out_shp_file_full = os.path.join(outdir, tshpname + '_out.shp')

    outshpdirname = os.path.dirname(out_shp_file_full)
    print outshpdirname
    if not os.path.exists(outshpdirname):
        os.makedirs(outshpdirname)
    command += " -osf " + out_shp_file_full
    
    if(parsed_parms.has_key('missingfeatures')):
        if((parsed_parms['missingfeatures'] == 'True') or (parsed_parms['missingfeatures'] == 'true')):
            command += " -mf "
        else:
            if(not os.path.isfile(full_inputshpname)):
                status_string = '{"status":"failed","reason":"no input shapefile and missing features is not set"}'
                json.dumps(status_string, status_json_file) 
                status_json_file.close()
                print 'No input shapefile exists and missing features is not true'
                return
    else:
        if(not os.path.isfile(full_inputshpname)):
                status_string = '{"status":"failed","reason":"no input shapefile and missing features is not set"}' 
                json.dumps(status_string, status_json_file) 
                status_json_file.close()
                print 'No input shapefile exists and missing features is not true'
                return

    sup_exe = "/dglabs/bin/dglabs/GeoTracker_Drivers/Release_develop_x64/CostDriver_Release_develop_x64"
    if(parsed_parms.has_key('supportexecutable')):
        sup_exe = parsed_parms['supportexecutable']
    command += " -supExe " + sup_exe 
    command += " -buildSupport" 

    for this_file in files:
        command += " -f " + this_file
        if os.path.exists(out_shp_file_full):
            removeShpfile(full_inputshpname)
            renameShpfile(out_shp_file_full, full_inputshpname)

        print command
        app_status = os.system(command)

    if(app_status == 0):
        status_string = '{"status":"success"}'
    else:
        print 'application fail'
        status_string = '{"status":"failed","reason" : "fail code returned by application system call."}'
    if(not status_json_file.closed):
        status_json_file.close()
    if(os.path.exists(status_path)):
        os.remove(status_path)
    status_json_file = open(status_path,'wb')
    json.dump(json.loads(status_string), status_json_file) 
    status_json_file.close()

if __name__ == '__main__':
    sys.exit(main())
