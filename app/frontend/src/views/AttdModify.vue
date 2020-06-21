<template>
  <div class="home">
    <ModifyAttdForm :attdrec = 'attd' @attdupd='updaterec'> </ModifyAttdForm>
  </div>

</template>

<script>
// @ is an alias to /src
import ModifyAttdForm from '@/components/ModifyAttd.vue';

export default {
  name: 'attdModify',
  props: {
    attd: Array,
  },
  components: {
    ModifyAttdForm,
  },
  methods: {
    updaterec(modattd) {
      alert(modattd);
    },
  },
};
</script>
