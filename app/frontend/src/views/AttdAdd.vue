<template>
  <div class="home">
    <table>
      <tr v-for='stud in studlist' :key = 'stud.id'>
         <ManAttdList :stud='stud'> </ManAttdList>
      </tr>
    </table>
  </div>
</template>

<script>
// @ is an alias to /src
import ManAttdList from '@/components/AddAttdManual.vue';

export default {
  name: 'AddAttdFace',
  props: { studlist: Array },
  components: {
    ManAttdList,
  },
  methods: {
    validate(attdrec) {
      alert(attdrec);
    },
  },
};
</script>
