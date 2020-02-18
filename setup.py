import cx_Freeze

executables = [cx_Freeze.Executable("RiverCrossing.py")]

cx_Freeze.setup(
	name = "River Crossing",
	options = {
		"build_exe": {
			"packages" : ["pygame", "random", "configparser"], 
			"include_files" : ["config/", "res/"]
		}
	},
	executables = executables
)
