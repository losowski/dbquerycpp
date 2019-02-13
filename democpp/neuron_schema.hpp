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
		NeuronSchema(const string & connection);
		~NeuronSchema(void);
	public:
		//void connect(void);
		shared_ptr<tBody> gtBody(int primaryKey);
		
};
}
#endif //NEURON_SCHEMA_HPP
