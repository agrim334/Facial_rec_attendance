<template>
  <div class="home">
    <AddDeptForm @courseadd="validate">
    </AddDeptForm>
  </div>
</template>

<script>
// @ is an alias to /src
import AddDeptForm from '@/components/AddDept.vue';

export default {
  name: 'AddDept',
  components: {
    AddDeptForm,
  },
  methods: {
    validate(newdept) {
      if (newdept.did === null || newdept.did === '') {
        alert('Fill in user name');
      }
      if (newdept.name === null || newdept.name === '') {
        alert('Fill in first name');
      }
    },
  },
};
</script>
