#ifndef NEURON_SCHEMA_HPP
#define NEURON_SCHEMA_HPP

#include <string>
#include <list>
#include <map>
#include <set>
#include <tuple>

#include "dbconnection.hpp"

#include "tbody.hpp"

using namespace std;
using namespace dbquery;

namespace neuronSchema {

class NeuronSchema : public dbquery::DBConnection
{
	public:
		NeuronSchema(string username, string password);
		~NeuronSchema(void);
	public:
		//void connect(void);
		tBody build_tBody(int primaryKey);
		
};
}
#endif //NEURON_SCHEMA_HPP
