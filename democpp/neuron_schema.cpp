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
ptBody NeuronSchema::gtBody(int primaryKey)
{
	shared_ptr<tBody> obj(new tBody(this->m_dbconnection, primaryKey) );
	obj->selectRow();
	return obj;
}

//tIndividual
ptIndividual NeuronSchema::gtIndividual(int primaryKey)
{
	shared_ptr<tIndividual> obj(new tIndividual(this->m_dbconnection, primaryKey) );
	obj->selectRow();
	return obj;
}

paptIndividual NeuronSchema::gtIndividualbytBody(const tBody & body)
{
	return tIndividual::gtIndividualsFromBody(this->m_dbconnection, body);

}

}
