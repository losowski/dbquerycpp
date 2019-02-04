#include "neuron_schema.hpp"
using namespace std;

namespace neuronSchema {

NeuronSchema::NeuronSchema(const string & connection):
	dbquery::DBConnection(connection)
{
}

NeuronSchema::~NeuronSchema(void)
{
}

tBody const * NeuronSchema::build_tBody(int primaryKey)
{
	tBody const * obj = new tBody(this->m_dbconnection, primaryKey);
	return obj;
}

}
