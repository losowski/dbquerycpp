#ifndef NEURON_SCHEMA_TBODY_HPP
#define NEURON_SCHEMA_TBODY_HPP

#include <string>

#include "dbresult.hpp"

using namespace std;
using namespace dbquery;

namespace neuronSchema {

class tBody : public DBResult
{
	public:
		tBody(pqxx::connection * db);
		tBody(pqxx::connection * db, const int primaryKey);
		~tBody(void);
	public:
		//SELECT
		void selectRowSQL(pqxx::work* txn);
		//DELETE
		void deleteRowSQL(pqxx::work* txn, int primaryKey);
		//UPDATE
		void updateRowSQL(pqxx::work* txn);
		//INSERT
		void insertRowSQL(pqxx::work* txn);
	public:
		int 		id;
		string		text;
};
}
#endif //NEURON_SCHEMA_TBODY_HPP
