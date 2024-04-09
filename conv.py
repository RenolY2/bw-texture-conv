import argparse
import sys 
import os 
import bwtex 


if __name__ == "__main__":
    

    parser = argparse.ArgumentParser()
    parser.add_argument("input",
                        help="Path to texture")
    parser.add_argument('--bw1',
                        action='store_true')
    parser.add_argument('--bw2',
                        action='store_true')
    parser.add_argument("-f", "--format", default=None, 
                        help=("Format of new BW1/BW2 texture. Default: DXT1 \n"
                                "For BW1: One of DXT1, P8, RGBA.\n" 
                                "For BW2: One of DXT1, P4, P8, I4, I8, IA4, IA8, RGBA"))
    parser.add_argument("output", default=None, nargs = '?',
                        help=("Path to output") )

    args = parser.parse_args()
    assert (args.bw1 or args.bw2) and not (args.bw1 and args.bw2)
    #in_path = sys.argv[1]
    in_path = args.input 
    
    if in_path.endswith(".texture"):
        with open(in_path, "rb") as f:
            if args.bw1:
                tex = bwtex.BW1Texture.from_file(f)  
            else:
                tex = bwtex.BW2Texture.from_file(f)  
        print("Texture format:", tex.fmt)
        if args.output is not None:
            outpath = args.output 
        else:
            outpath = in_path.replace(".texture", "")+"."+tex.fmt+".png"
        tex.mipmaps[0].save(outpath)
        """if len(tex.mipmaps) > 1:
            print("saved mipmap")
            for i, mip in enumerate(tex.mipmaps[1:]):
                mip.save(in_path+".mip{0}".format(i)+".png")"""
    else:
        settings = os.path.basename(in_path).split(".")
        if args.format is None:
            if len(settings) > 2:
                fmt = settings[1]
                if fmt not in bwtex.STRTOFORMAT:
                    fmt = "DXT1"
            else:
                fmt = "DXT1"
        else:
            fmt = args.format
        print("Converting to format", fmt)
        if args.bw1:
            tex = bwtex.BW1Texture.from_path(path=in_path, name=settings[0], fmt=fmt)
        else:
            tex = bwtex.BW2Texture.from_path(path=in_path, name=settings[0], fmt=fmt)
        
        if args.output is None:
            outpath = in_path+".texture"
        else:
            outpath = args.output
        
        with open(outpath, "wb") as f:
            tex.write(f)