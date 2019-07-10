upd:{[tabname;tabdata] show tabname; show tabdata}

h:@[hopen;`::9568;{-2"Failed to open connection to publisher on port 9568: ",
		     x,". Please ensure publisher is running"; 
		     exit 1}]

h(`.u.sub;`;`)		     