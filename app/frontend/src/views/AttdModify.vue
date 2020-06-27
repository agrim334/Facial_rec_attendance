<template>
  <div class="home">
    <ModifyAttdForm :attdrec = 'attd' @attdupd='updaterec'> </ModifyAttdForm>
  </div>

</template>

<script>
// @ is an alias to /src
import axios from 'axios';
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
      const path = 'http://localhost:5000/attd/modify_attd_json';
      axios.post(path, { old: this.attd, new: modattd })
        .then((res) => {
          console.log(res);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
