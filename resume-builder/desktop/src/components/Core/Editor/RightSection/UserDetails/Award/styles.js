import { StyleSheet } from 'aphrodite';

export const styles = StyleSheet.create({
     h2 :{
    margin: [0,10, !important],
    fontWeight: 1.8rem,
    fontWeight: 700
  },

  iconAwardsCursor: {
    cursor: pointer
  },

addButtonRight: {
    marginLeft: auto,
    marginRight: 20
        
    &:before {
      content: '+';
      font-size: 1.8rem;
      padding-right: 5px;
    }
  },

  tillToday: {
    color: $txt2;
    margin: 10px 0 0 0;
    display: block;
    text-align: right;

    input: {
      margin-right: 5px;
    }
  }
})