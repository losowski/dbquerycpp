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

//tBody
shared_ptr<tBody> NeuronSchema::gtBody(int primaryKey)
{
	shared_ptr<tBody> obj(new tBody(this->m_dbconnection, primaryKey) );
	obj->selectRow();
	return obj;
}

//tIndividual
shared_ptr<tIndividual> NeuronSchema::gtIndividual(int primaryKey)
{
	shared_ptr<tIndividual> obj(new tIndividual(this->m_dbconnection, primaryKey) );
	obj->selectRow();
	return obj;
}

shared_ptr <tIndividuals_t> gtIndividualbytBody(int bodyId)
{
	//TODO: Figure out how to generate this list sensibly
	// Needs some SQL here which breaks the design
}

}
