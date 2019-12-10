## Dijkstra 
This README explains the execution flow of the algorithm and how much memory it occupies.

#### Variables
* TARGET_INDEX:  
	* i, j, size,up, val, min;  
* TARGET_TYPE:  
	* new_dist, dist[size], a[size, size];

#b = number of bytes used by a given data type (e.g. int8_t, int16_t)  
#index = number of variables used as an index  

Total Memory > (#index * #b) + (size * #b) + (size * size * #b)
