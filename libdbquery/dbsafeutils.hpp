#ifndef DBSAFEUTILS_HPP
#define DBSAFEUTILS_HPP

/*
 * Utilities to safely intepret the DB input
 * Throws on badly formatted data
*/
#include <regex>

#include "dbutils.hpp"
#include "dbexceptionBadData.hpp"

using namespace std;

namespace dbquery {

static const regex REGEX_SIGNED_INT ("[-+]?[:digit:]+");
static const regex REGEX_SIGNED_ALPHANUM ("[_[:alnum:]]+");
static const regex REGEX_BASIC_STRING ("\\S+");

class DBSafeUtils : public DBUtils
{
	public:
		DBSafeUtils(void);
		~DBSafeUtils(void);
	public:
		static void safeToInt(int * integer, const pqxx::field & fieldValue);
		static void safeToString(string * str, const pqxx::field & fieldValue);
		static void safeToString(string * str, const pqxx::field & fieldValue, const regex & regexExpression);
	private:
		static void checkValidInput(const char * input, const regex & regexExpression);
		static void checkValidInput(const string & input, const regex & regexExpression);
};

}
#endif //DBSAFEUTILS_HPP
