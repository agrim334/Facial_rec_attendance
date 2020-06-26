<template>
 <div>
    <label> {{ stud.id }} </label>
    <input type='radio' id='absent' name='stud.id' value = '0' v-model = 'stud.status'>
    <label for='absent'> Absent </label>

    <input type='radio' id='present' name='stud.id' value = '1' v-model = 'stud.status'>
    <label for='present'> Present </label>

    <br>
 </div>
</template>

<script>
export default {
  name: 'ManAttdList',
  props: { stud: Array },
};
</script>
