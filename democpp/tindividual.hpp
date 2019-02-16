#ifndef NEURON_SCHEMA_TINDIVIDUAL_HPP
#define NEURON_SCHEMA_TINDIVIDUAL_HPP

#include "dbresult.hpp"
#include "dbsafeutils.hpp"

#include "tbody.hpp"

using namespace std;
using namespace dbquery;

namespace neuronSchema {

class tIndividual;

typedef shared_ptr<tIndividual> ptIndividual;
typedef vector < ptIndividual >  aptIndividual;
typedef shared_ptr < aptIndividual>  paptIndividual;

class tIndividual : public DBResult
{
	public:
		tIndividual(pqxx::connection * db);
		tIndividual(pqxx::connection * db, const int primaryKey);
		tIndividual(pqxx::connection * db, int id, int body_id, const string & name);
		~tIndividual(void);
	public:
		//SELECT
		void selectRowSQL(pqxx::work* txn);
		//DELETE
		void deleteRowSQL(pqxx::work* txn, int primaryKey);
		//UPDATE
		void updateRowSQL(pqxx::work* txn);
		//INSERT
		void insertRowSQL(pqxx::work* txn);
		//Schema Functions
		shared_ptr<tBody> gtBody(void);
		static paptIndividual gtIndividualsFromBody(pqxx::connection* db, const tBody & body);
	public:
		int 		id;
		int 		body_id;
		string		name;
};
}
#endif //NEURON_SCHEMA_TINDIVIDUAL_HPP
