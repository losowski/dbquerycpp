#ifndef NEURON_SCHEMA_TBODY_HPP
#define NEURON_SCHEMA_TBODY_HPP

#include <string>
#include <list>
#include <map>
#include <set>
#include <tuple>


#include "dbresult.hpp"

using namespace std;
using namespace dbquery;

namespace neuronSchema {

class tBody : public DBResult
{
	public:
		tBody(int primaryKey);
		~tBody(void);
	public:
		//SELECT
		void getRow(void);
		//DELETE
		void deleteRow(int primaryKey);
		//UPDATE
		void saveRow(void);
		//INSERT
		void addRow(void);
	public:
		int 		id;
		string		text;
};
}
#endif //NEURON_SCHEMA_TBODY_HPP
