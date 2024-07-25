<template>
  <div id=floating-panel style="width: 560px">
    <div class="q-pa-md">
    <div class="row q-pb-md">
      <div v-if="modifier === 'Author'">
      <q-btn outline color="primary" @click="modifier = 'Author'" class="col-grow">Author</q-btn>
      </div>
      <div v-else>
        <q-btn flat color="primary" @click="modifier = 'Author'" class="col-grow">Author</q-btn>
      </div>
      <div v-if="modifier === 'Year'">
        <q-btn outline color="primary" @click="modifier = 'Year'" class="col-grow">Year</q-btn>
      </div>
      <div v-else>
        <q-btn flat color="primary" @click="modifier = 'Year'" class="col-grow">Year</q-btn>
      </div>
      <div v-if="modifier === 'Language'">
        <q-btn outline color="primary" @click="modifier = 'Language'" class="col-grow">Language</q-btn>
      </div>
      <div v-else>
        <q-btn flat color="primary" @click="modifier = 'Language'" class="col-grow">Language</q-btn>
      </div>
      <div v-if="modifier === '('">
        <q-btn outline color="primary" @click="modifier = '('" class="col-grow">(</q-btn>
      </div>
      <div v-else>
        <q-btn flat color="primary" @click="modifier = '('" class="col-grow">(</q-btn>
      </div>
      <div v-if="modifier === ')'">
        <q-btn outline color="primary" @click="modifier = ')'" class="col-grow">)</q-btn>
      </div>
      <div v-else>
        <q-btn flat color="primary" @click="modifier = ')'" class="col-grow">)</q-btn>
      </div>

    </div>
    <div class="row q-gutter-sm">
      <q-select v-if="modifier !==  ')'"
        class="col-3"
        rounded
        outlined
        v-model="booleanOperator"
        :options="['None', 'AND', 'OR']"
        color="secondary"
      >
      </q-select>
      <div v-if="modifier === 'Year'" class="col-grow" style="margin-right: 20px; margin-left: 18px">
        <q-range
          v-model="range"
          label
          color="secondary"
          :min=2017
          :max=2021
          :step="1"
          markers=""
        >
        </q-range>
      </div>
      <div v-else-if="modifier === 'Language'" class="col-grow">
        <q-select
          filled
          v-model="language"
          :options="options"
          label="Language"
          color="primary"
        >
        </q-select>
      </div>
      <div v-else-if="modifier === 'Author'" class="col-grow">
        <div class="row q-gutter-sm no-wrap">
          <q-input
            class="col-grow"
            outlined
            v-model="authorName"
            label="Name"
          ></q-input>
          <q-input
            class="col-grow"
            outlined
            v-model="authorLastName"
            label="Last name"
          ></q-input>
        </div>
      </div>
      <div v-else-if="modifier === '('" class="col-grow">
        <q-chip square size="xl">(</q-chip>
      </div>
      <div v-else-if="modifier === ')'" class="col-grow">
        <q-chip square size="xl">)</q-chip>
      </div>
    </div>
  </div>
    <div class="row no-wrap">
      <q-btn style="border-radius: 0px 0px 0px 8px" outline class="col-6"  icon="done" @click="saveModifier" color="positive"></q-btn>
      <q-btn style="border-radius: 0px 0px 8px 0px" outline class="col-6"  icon="clear" @click="resetModifier" color="negative"></q-btn>
    </div>
  </div>

</template>


<script>

import {computed, onMounted, reactive, toRefs, ref} from "vue";
import {useStore} from "vuex";

const options = ['arabic', 'english', 'german', 'spanish', 'finnish', 'french', 'italian', 'dutch', 'norwegian', 'portuguese']

export default {
  name: "addModifier",
  components: {},
  emits: [
    'setRenderModify',
    'addOperator'
  ],
  setup(props, {emit}) {
    const resetModifier = function () {
      emit('setRenderModify', false)
    }
    const saveModifier = function () {
      if (state.modifier === 'Author') {
        const authorObj = {
          label : 'author: ' + state.authorName.trim() + ' ' + state.authorLastName.trim(),
          type : 'Author',
          operator: state.booleanOperator,
          name : state.authorName.trim(),
          lastName : state.authorLastName.trim(),
        }
        emit('addOperator', authorObj)
      } else if (state.modifier === 'Year') {
        const yearObj = {
          label : 'year: ' + state.range.min + '-' + state.range.max,
          type : 'Year',
          operator: state.booleanOperator,
          min : state.range.min,
          max : state.range.max,
        }
        emit('addOperator', yearObj)
      } else if (state.modifier === 'Language') {

        const languageObj = {
          label : 'lang: ' + state.language,
          type : 'Language',
          operator: state.booleanOperator,
          language : state.language,
        }
        emit('addOperator', languageObj)
      } else if (state.modifier === 'Title') {
        const titleObj = {
          label : 'title: ' + state.title,
          type : 'Title',
          operator: state.booleanOperator,
          title : state.title,
        }
        emit('addOperator', titleObj)
      } else if (state.modifier === '(') {
        const openParenthesesObj = {
          label: '(',
          type: '(',
          operator: state.booleanOperator,
        }
        emit('addOperator', openParenthesesObj)
      } else if (state.modifier === ')') {
        const closedParenthesesObj = {
          label: ')',
          type: ')',
          operator: 'None'
        }
        emit('addOperator', closedParenthesesObj)
      }

      emit('setRenderModify', false)
    }
    let state = reactive({
      counter : 0,
      range : ref({
        min: 2017,
        max: 2021,
      }),
      language: "",
      title: "",
      authorName: '',
      authorLastName: '',
      booleanOperator: 'None',
      modifier: "Year",
      options,
      resetModifier,
      saveModifier,
    });
    return toRefs(state);
  }
}
</script>

<style>

#floating-panel {
  position: absolute;
  border-radius: 8px;
  top: 500px;
  left: 50%;
  background-color: white;

  transform: translateX(-50%) translateY(-50%);
}

</style>
