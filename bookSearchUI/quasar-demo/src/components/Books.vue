<template>
  <div class="q-pa-md">
    <q-table
      grid
      :card-container-class="cardContainerClass"
      :rows="books"
      row-key="name"
      hide-bottom
      hide-header
      v-model:pagination="pagination"
      no-data-label="No data"
    >
      <template v-slot:top="scope">
        <div class="row justify-between no-wrap full-width">

          <div class="row q-gutter-sm no-wrap">
            <q-input color="primary"
                     style="width: 400px"
                     outlined
                     v-on:keyup.enter="querySolr"
                     v-model="query"
                     label="Search a book">
              <template v-slot:before>
                <q-avatar>
                  <q-btn icon="search" @click="querySolr()" color="primary"></q-btn>
                </q-avatar>
              </template>

            </q-input>
            <q-btn dense flat icon="add" @click="addModifier()" color="primary"></q-btn>

            <div class="column justify-center">
              <div class=" row q-gutter-xs">
                <div v-for="(chip, index) in operators" :key="chip" class="column justify-center">

                  <div v-if="chip.type === '('" class="column justify-center">
                    <q-chip dense color="white" class="no-margin" removable
                            @remove="operators.splice(index, 1)">
                      <q-avatar v-if="chip.operator === 'AND'" style="font-size: 20px" color="red" text-color="white">
                        &&
                      </q-avatar>
                      <q-avatar v-if="chip.operator === 'OR'" style="font-size: 20px" color="blue" text-color="white">
                        ||
                      </q-avatar>
                      <h4>(</h4>
                      <template v-slot:append>
                        <q-icon name="cancel" size="xs"></q-icon>
                      </template>
                    </q-chip>
                  </div>
                  <div v-else-if="chip.type === ')'" class="column justify-center">
                    <q-chip dense color="white" class="no-margin" removable
                            @remove="operators.splice(index, 1)">
                      <h4>)</h4>
                    </q-chip>
                  </div>
                  <div v-else-if="chip.type === 'Year'">
                    <q-chip class="no-margin" removable @remove="removeModifier(index)">
                      <q-avatar v-if="chip.operator === 'AND'" style="font-size: 24px" color="red" text-color="white">
                        &&
                      </q-avatar>
                      <q-avatar v-if="chip.operator === 'OR'" style="font-size: 24px" color="blue" text-color="white">
                        ||
                      </q-avatar>
                      <div v-if="chip.min !== chip.max"> {{ chip.label }}</div>
                      <div v-else>{{'year:' + chip.min}}</div>
                    </q-chip>
                  </div>
                  <div v-else>
                    <q-chip class="no-margin" removable @remove="removeModifier(index)">
                      <q-avatar v-if="chip.operator === 'AND'" style="font-size: 24px" color="red" text-color="white">
                        &&
                      </q-avatar>
                      <q-avatar v-if="chip.operator === 'OR'" style="font-size: 24px" color="blue" text-color="white">
                        ||
                      </q-avatar>
                      {{ chip.label }}
                    </q-chip>

                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row q-gutter-sm no-wrap">
            <div class="column justify-center q-pr-md">
              <caption v-if="scope.pagination.page * scope.pagination.rowsPerPage < lengthBooks">
                {{scope.pagination.page * scope.pagination.rowsPerPage }} -
                <strong style="color: blue">{{ lengthBooks }}</strong> results
              </caption>
              <caption v-else>
                {{lengthBooks}} - <strong style="color: blue">{{ lengthBooks }}</strong> results
              </caption>
            </div>
            <q-btn
              style="color: blue; height: 50px"
              icon="chevron_left"
              :disable="scope.isFirstPage"
              @click="scope.prevPage">
            </q-btn>
            <q-btn
              style="color: blue; height: 50px"
              icon="chevron_right"
              :disable="scope.isLastPage"
              @click="scope.nextPage">
            </q-btn>
          </div>
        </div>
      </template>

      <template v-slot:item="props">
        <div class="q-pa-sm col-xs-12 col-sm-6 col-md-3">
          <q-card>
            <q-card-section class="q-pt-sm q-pb-sm">
              <div class="column justify-center">
                <a class="text-primary" :href="props.row.link" style="text-decoration: none">
                  <strong>
                  <WordHighLighter :splitBySpace="true"
                                   :query='query'>{{ props.row.title[0] }}
                  </WordHighLighter>
                  </strong>
                </a>
              </div>
            </q-card-section>
            <q-separator></q-separator>
            <q-card-section>
              <div class="q-pb-sm">
                <q-scroll-area id='scroll' style="height: 31px">
                  <div id=#scroll class="row q-gutter-xs no-wrap">
                    <div class="col-auto" v-for="author in props.row.authors" :key="author">
                      <q-chip v-if="authors.indexOf(author) === -1" color="secondary" text-color="white" class="no-margin"> {{ author }}</q-chip>
                      <q-chip v-if="authors.indexOf(author) !== -1" color="orange" text-color="white" class="no-margin"> {{ author }}</q-chip>
                    </div>
                  </div>
                </q-scroll-area>
              </div>
              <q-scroll-area class="q-pb-sm"
                style="height: 90px">
                <WordHighLighter :splitBySpace="true"
                                 :query='query'>
                  {{ props.row.description[0] }}
                </WordHighLighter>
              </q-scroll-area>
              <q-expansion-item
                class="no-padding"
                style="color: blue"
                label="Subjects"
              >
                <q-card>
                  <q-card-section>
                    <WordHighLighter :splitBySpace="true"
                                     :query='query'>
                      {{ 'Subjects: ' + props.row.subjects[0] }}
                    </WordHighLighter>
                    <p></p>
                    <WordHighLighter :splitBySpace="true"
                                     :query='query' style="color: green">
                      {{ 'Other data: ' + props.row.allOtherData[0] }}
                    </WordHighLighter>
                    <div v-if="debug">
                      <caption style="color: red">{{"Score:" +props.row.score}}</caption>
                    </div>
                  </q-card-section>
                </q-card>
              </q-expansion-item>
              <div class="row reverse q-pt-sm justify-between no-wrap">
                <q-chip v-if="years.indexOf(props.row.yearOfPublication[0]) === -1" class="no-margin"
                        outline color="primary" text-color="white">{{ props.row.yearOfPublication[0] }}
                </q-chip>
                <q-chip v-if="years.indexOf(props.row.yearOfPublication[0]) !== -1" class="no-margin"
                        outline color="orange" text-color="white">{{ props.row.yearOfPublication[0] }}
                </q-chip>
                <q-chip v-if="languages.indexOf(props.row.language[0]) === -1" class="no-margin">{{ props.row.language[0]}}</q-chip>
                <q-chip v-if="languages.indexOf(props.row.language[0]) !== -1" color="orange" class="no-margin">{{ props.row.language[0]}}</q-chip>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </template>
    </q-table>
    <div v-if="renderModify">
      <overlay-page></overlay-page>
      <add-modifier @setRenderModify="setRenderModify" @addOperator="addOperator"></add-modifier>
    </div>
  </div>
</template>


<script>
import {useStore} from "vuex";
import {computed, onMounted, reactive, ref, toRefs,} from "vue";
import {useQuasar} from "quasar";

import OverlayPage from "components/overlayPage";
import AddModifier from "components/addModifier";
import WordHighLighter from 'vue-word-highlighter'


export default {
  name: "Books",
  components: {AddModifier, OverlayPage, WordHighLighter},
  setup() {
    const $q = useQuasar()
    const store = useStore();

    const querySolr = async function () {
      await store.dispatch('solr/fetchContents', {
          query: state.query,
          operators: state.operators
        }
      ).catch(e => {
        throw e;
      });
    }

    onMounted(async () => {
      await store.dispatch('solr/fetchAll').catch(e => {
        throw e;
      });
    });

    const books = computed(() => store.getters["solr/retrievedData"]);
    const lengthBooks = computed(() => store.getters["solr/lengthData"]);

    const cardContainerClass = computed(() => {
      return $q.screen.gt.xs
        ? 'grid-masonry grid-masonry--' + ($q.screen.gt.sm ? '3' : '2')
        : null
    });

    const addOperator = function (operator) {

      state.operators.push(operator)

      state.authors = []
      state.years = []
      state.languages = []
      state.operators.forEach(function (entry) {
        if (entry.type === 'Language') {
          state.languages.push(entry.language)
        }
        if (entry.type === 'Year'){
          for (let i = entry.min; i <= entry.max; i++) {
            state.years.push(i)
          }
        } else if (entry.type === 'Author') {
          state.authors.push(entry.name + ' ' + entry.lastName)
        }
      })
    }

    const removeModifier = function(index) {

      const data = state.operators[index]


      if (data.type === 'Language') {
        const x = state.languages.findIndex(val => val === data.language)
        state.languages.splice(x, 1)
      } else if (data.type === 'Author') {
        const y = state.authors.findIndex(val => val === (data.name + ' ' + data.lastName))
        state.authors.splice(y, 1)
      } else if (data.type === 'Year') {
        for (let i = data.min; i <= data.max; i++) {
          const z = state.years.findIndex(val => val === i)
          state.years.splice(z, 1)
        }
      }
      state.operators.splice(index, 1)

    }

    const addModifier = function () {
      setRenderModify(true)
    }
    const setRenderModify = function (render) {
      state.renderModify = render
    }
    const getItemsPerPage = function () {
      if ($q.screen.lt.sm) {
        return 4
      }
      if ($q.screen.lt.md) {
        return 8
      }
      return 12
    }

    const pagination = ref({
      page: 1,
      rowsPerPage: getItemsPerPage()
    })

    let state = reactive({
      removeModifier,
      querySolr,
      addOperator,
      setRenderModify,
      addModifier,
      query: '',
      operators: [],
      authors: [],
      years: [],
      languages:[],
      renderModify: false,
      debug: true,
      lengthBooks,
      books,
      cardContainerClass,
      pagination,
      tableScope: null,
    });

    return toRefs(state);
  }
}
</script>

<style scoped>
#scroll {
  overflow: auto !important;
  overflow-y: hidden !important;
}
</style>

<style lang="scss">
.q-table__top {
  padding: 0px 8px 8px 8px;
}

.q-item {
  min-height: 5px;
  padding: 0px 0px 0px 0px;
}
</style>
