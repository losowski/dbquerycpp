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

shared_ptr<tBody> NeuronSchema::tBody(int primaryKey)
{
	shared_ptr<tBody> obj(new tBody(this->m_dbconnection, primaryKey));
	return obj;
}

}
