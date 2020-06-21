<template>
  <div class="home">
    <table>
      <tr v-for='dept in depts' :key='dept.did'>
        <deptrec :dept='dept' @updrec='updaterec' @delrec='deleterec'></deptrec>
      </tr>
    </table>
    <button id='add' @click='addrec'>Add Depts</button>
  </div>

</template>

<script>
// @ is an alias to /src
import deptrec from '@/components/RUDDept.vue';

export default {
  name: 'DeptTable',
  props: {
    depts: Array,
  },
  components: {
    deptrec,
  },
  methods: {
    updaterec(Deptdat) {
      alert(Deptdat);
    },
    deleterec(Deptdat) {
      alert(Deptdat);
    },
    addrec() {
      alert('sdcf');
    },
  },
};
</script>
