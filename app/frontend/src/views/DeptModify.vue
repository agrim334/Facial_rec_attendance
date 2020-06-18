<template>
  <div class="home">
    <ModifyDeptForm :deptrec = 'dept' @deptupd='updaterec'> </ModifyDeptForm>
  </div>

</template>

<script>
// @ is an alias to /src
import ModifyDeptForm from '@/components/ModifyDept.vue';

export default {
  name: 'DeptModify',
  props: {
    dept: Array,
  },
  components: {
    ModifyDeptForm,
  },
  methods: {
    updaterec(modDept) {
      alert(modDept);
    },
  },
};
</script>
