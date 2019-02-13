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

shared_ptr<tBody> NeuronSchema::gtBody(int primaryKey)
{
	shared_ptr<tBody> obj(new tBody(this->m_dbconnection, primaryKey) );
	return obj;
}

shared_ptr<tIndividual> NeuronSchema::gtIndividual(int primaryKey)
{
	shared_ptr<tIndividual> obj(new tIndividual(this->m_dbconnection, primaryKey) );
	return obj;
}

}
