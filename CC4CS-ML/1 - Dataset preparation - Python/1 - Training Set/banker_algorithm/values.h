#ifndef VALUES
#define VALUES
	enum{ n_resources = 4 };
	uint8_t available[n_resources]
	= {0, 93, 180, 154};
	enum{ n_process = 2 };
	uint8_t max[n_process][n_resources]
	= {{228, 79, 21, 188},
	   {92, 140, 246, 104}};
	uint8_t allocated[n_process][n_resources]
	= {{46, 43, 36, 3},
	   {7, 12, 224, 189}};
#endif