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

tBody NeuronSchema::build_tBody(int primaryKey)
{
}

}
