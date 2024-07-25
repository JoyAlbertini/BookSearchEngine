import { createStore } from 'vuex';

import solr from './solr';

export default createStore({
  modules: {
   solr
  },

  // enable strict mode (adds overhead!)
  // for dev mode and --debug builds only
  strict: process.env.DEBUGGING
});
