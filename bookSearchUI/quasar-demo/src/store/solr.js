import $ from 'jquery'

const REPO = 'bookTest2'

const languagesSuffix = ['_txt_ar', '_txt_en', '_txt_de', '_txt_es', '_txt_fi', '_txt_fr', '_txt_it', '_txt_nl', '_txt_no', '_txt_pt',]

export default {
  namespaced: true,
  state: {
    retrievedData: [],
    lengthData : 0
  },
  mutations: {
    setContents(state, data) {
      let parsedData = []

      data.response.docs.forEach(function(entry) {

        const current = {}
        current.link = entry.link

        current.yearOfPublication = entry.yearOfPublication
        current.authors = entry.authors
        current.allOtherData = entry.allOtherData
        current.score = entry.score
        current.language = entry.language

        switch (entry.language[0]) {
          case 'arabic':
            current.description = [entry.description_txt_ar];
            current.subjects = [entry.subjects_txt_ar];
            current.title = [entry.title_txt_ar];
            break;
          case 'english':
            current.description = [entry.description_txt_en];
            current.subjects = [entry.subjects_txt_en];
            current.title = [entry.title_txt_en];
            break;
          case 'german':
            current.description = [entry.description_txt_de];
            current.subjects = [entry.subjects_txt_de];
            current.title = [entry.title_txt_de];
            break;
          case 'spanish':
            current.description = [entry.description_txt_es];
            current.subjects = [entry.subjects_txt_es];
            current.title = [entry.title_txt_es];
            break;
          case 'finnish':
            current.description = [entry.description_txt_fi];
            current.subjects = [entry.subjects_txt_fi];
            current.title = [entry.title_txt_fi];
            break;
          case 'french':
            current.description = [entry.description_txt_fr];
            current.subjects = [entry.subjects_txt_fr];
            current.title = [entry.title_txt_fr];
            break;
          case 'italian':
            current.description = [entry.description_txt_it];
            current.subjects = [entry.subjects_txt_it];
            current.title = [entry.title_txt_it];
            break;
          case 'dutch':
            current.description = [entry.description_txt_nl];
            current.subjects = [entry.subjects_txt_nl];
            current.title = [entry.title_txt_nl];
            break;
          case 'norwegian':
            current.description = [entry.description_txt_nl];
            current.subjects = [entry.subjects_txt_nl];
            current.title = [entry.title_txt_nl];
            break;
          case 'portuguese':
            current.description = [entry.description_txt_pt];
            current.subjects = [entry.subjects_txt_pt];
            current.title = [entry.title_txt_pt];
            break;
          default:
            current.description = ['None']
            current.subjects = ['None']
            current.title = ['None']
        }
        parsedData.push(current)
      })
      state.retrievedData = parsedData

      state.lenghtData = parsedData.length
    },
  },
  actions: {

    // Performed only on page start to give full the page with some results
    fetchAll: async ({commit}) => {
      const all = 'http://localhost:8983/solr/'+ REPO +
        '/select?fl=*%20score&indent=true&q.op=OR&q=*%3A*&rows=100&wt=json'
      $.getJSON(all, function (response) {
        commit("setContents", response);
      })
    },

    fetchContents: async ({commit}, {query, operators}) => {
      const encodeOR = encodeURI(' || ')
      const encodeAND ='%20%26%26%20' // ' && ' (encodeURI does not working)
      const encodePlus = '%20%2B%20' // ' + '

      let baseQuery = ''
      let operatorQueries = ''
      const queryEmpty = !query.trim().length > 0
      const operatorEmpty = queryEmpty.length === 0


      if (!queryEmpty) {

        // Query encode --------------------------------------------------------------------------------------------------
        // 1) parse the query, add ORs between each word of the query, so that we can retrieve the max number of matching
        // documents : queryORWordsSolr
        // 2) parse the query, add parentheses between words : queryAndWordSolr
        // 3) parse the query, add Ands between each word of the query : queryAndWorldSolr2

        const words = query.trim().split(" ")

        let queryORWordsSolr = '('
        let queryAndWordSolr = '"'
        let queryAndWorldSolr2 = '('
        let N = words.length
        for (let i = 0; i < N; i++) {
          if (i === N - 1) {
            queryAndWorldSolr2 += words[i] + ')'
            queryAndWordSolr +=  '(' + words[i] + ')"'
            queryORWordsSolr += words[i] + ')'
          } else {
            queryAndWorldSolr2 += words[i] + encodeAND
            queryAndWordSolr += '(' + words[i] + ') '
            queryORWordsSolr += words[i] + ' || '
          }
        }
        //encode in URI
        const encodedOrWordQuerySolr = encodeURI(queryORWordsSolr)
        const encodedAndWordQuerySolrAllWord = queryAndWorldSolr2
        const encodedAndWordQuerySolrProximity = encodeURI(queryAndWordSolr)


        // For each title subjects description we need to append the suffix language ( example "_txt_en"),all
        // those language specific fields are ored together so that they can match any language that the user
        // input in the query
        // The language specific field perform varies parsing in solr, giving the best result matching the terms in the
        // query

        // define multiply scores
        const boostTitle = encodeURI('^2.1')
        const boostSubject = encodeURI('^2.1')
        const boostDescription = encodeURI('^1.7')

        baseQuery = '('
        N = languagesSuffix.length
        for (let i = 0; i < N; i++) {
          baseQuery +=
             '('
                 // 1) ored words ---> increase recall
              + 'title' + languagesSuffix[i] + '%3A' + encodedOrWordQuerySolr
                 // proximity of words ---> increase precision, by increasing the score of such words
                 + encodePlus
              + 'title' + languagesSuffix[i] + '%3A' + encodedAndWordQuerySolrProximity + '~' + words.length
                 // and all words ---> book which contains all words should have an higher score --> increase precision
                 + encodePlus
              + 'title' + languagesSuffix[i] + '%3A' + encodedAndWordQuerySolrAllWord
            + ')' + boostTitle  // boost title score
              + encodeOR //
            + '('
               + 'subjects' + languagesSuffix[i] + '%3A' + encodedOrWordQuerySolr
                  + encodePlus
               + 'subjects' + languagesSuffix[i] + '%3A' + encodedAndWordQuerySolrProximity + '~' + words.length
                  + encodePlus
               + 'subjects' + languagesSuffix[i] + '%3A' + encodedAndWordQuerySolrAllWord
            + ')' + boostSubject // boost subject score
              + encodeOR
            + '('
              + 'description' + languagesSuffix[i] + '%3A' + encodedOrWordQuerySolr
                 + encodePlus
              + 'description' + languagesSuffix[i] + '%3A' + encodedAndWordQuerySolrProximity + '~' + words.length
                 + encodePlus
              + 'description' + languagesSuffix[i] + '%3A' + encodedAndWordQuerySolrAllWord
            + ')' + boostDescription // boost description score
            + encodeOR
        }
        // add allOtherData
        baseQuery +=  'allOtherData%3A' + encodedOrWordQuerySolr + ')'
      }

      if (!operatorEmpty) {

        // Operator encode -----------------------------------------------------------------------------------------------
        // I define as operators the extra AND OR operation on Language Year that you can add to the system, those are
        // parsed here

        let operatorQueriesArr = []
        for (let i = 0; i < operators.length; i++) {
          let encodeOperator

          if (operators[i].operator === 'AND') {
            encodeOperator = encodeAND
          } else if (operators[i].operator === 'OR') {
            encodeOperator = encodeOR
          } else {
            encodeOperator = ''
          }
          // first element shouldn't have the operator if the query is empty
          if (i === 0) {
            encodeOperator = queryEmpty ? '' : encodeOperator
          }
          switch (operators[i].type) {
            case '(':
              operatorQueriesArr.push(encodeOperator + '(')
              break;
            case ')':
              operatorQueriesArr.push(')')
              break;
            case "Language":
              operatorQueriesArr.push(encodeOperator + 'language%3A' + encodeURI(operators[i].language))
              break;
            case "Author":
              operatorQueriesArr.push(encodeOperator + 'authors%3A' + encodeURI('"'
                + operators[i].name + ' ' + operators[i].lastName + '"'))
              break;
            case "Year":
              let years = encodeOperator + '('
              for (let z = operators[i].min; z <= operators[i].max; z++) {
                if (z === operators[i].max) {
                  years += 'yearOfPublication%3A' + z + ')'
                } else {
                  years += 'yearOfPublication%3A' + z + encodeOR
                }
              }
              operatorQueriesArr.push(years)
          }
        }
        operatorQueries = operatorQueriesArr.join('')
      }


      // Perform the request to solr  ----------------------------------------------------------------------------------
      const url ='http://localhost:8983/solr/'+ REPO + '/select?' //data repository
        + '&defType=lucene' // query matching system
        + '&fl=*%20score' // add score
        + '&indent=true' // indent
        + '&q.op=OR'  // base operation OR
        + '&q=' + baseQuery // query
        + operatorQueries // additional operators
        +'&rows=20000'
        +'&sort=score%20desc' // sort based on score desc
        +'&wt=json' // output json


      console.log(url)
      // perform the query to solr
      $.ajax({
        url: url,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(response){
          commit("setContents", response);
          },
        error: function(errMsg) {
          alert("Error: query not accepted by solr, check operators");
        }
      });

    },
  },
  getters: {
    retrievedData: (state) => state.retrievedData || [],
    lengthData: (state) => state.lenghtData || 0
  }
}
