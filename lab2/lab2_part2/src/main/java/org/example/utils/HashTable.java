package org.example.utils;


import java.util.ArrayList;
import java.util.List;

public class HashTable<T> {
    private static final int INITIAL_CAPACITY = 30;
    private static final double LOAD_FACTOR = 0.7;
    private int size;
    private List<List<T>> buckets;

    public HashTable(int size) {
        this.size = INITIAL_CAPACITY;
        this.buckets = new ArrayList<>(size);
        for (int i = 0; i < this.size; i++) {
            this.buckets.add(i, new ArrayList<>());
        }
    }

    private int hash(T elem) {
        int value = elem.hashCode() % size;
        return Math.abs(value);
    }

    private void rehash() {
        int newSize = (int) (size * 1.1);
        List<List<T>> newBuckets = new ArrayList<>(newSize);

        for (int i = 0; i < newSize; i++) {
            newBuckets.add(new ArrayList<>());
        }

        for (List<T> bucket : buckets) {
            for (T elem : bucket) {
                int posInBucket = Math.abs(elem.hashCode()) % newSize;
                newBuckets.get(posInBucket).add(elem);
            }
        }

        size = newSize;
        buckets = newBuckets;
    }

    public Pair<Integer, Integer> get(T elem) {
        int posInBucket = hash(elem);
        for (int i = 0; i < this.buckets.get(posInBucket).size(); i++) {
            T bucketElem = this.buckets.get(posInBucket).get(i);
            if (bucketElem.equals(elem)) {
                return new Pair<>(posInBucket, i);
            }
        }
        return null;
    }

    public Pair<Integer, Integer> add(T elem) {
        if((double) size / buckets.size() >= LOAD_FACTOR){
            rehash();
        }
        Pair<Integer, Integer> lookup = get(elem);
        if (lookup != null) {
            return lookup;
        }
        int posInBucket = hash(elem);
        int posInList = this.buckets.get(posInBucket).size();
        this.buckets.get(posInBucket).add(elem);
        return new Pair<>(posInBucket, posInList);
    }

    public T findByPair(int posInBucket, int posInList) throws Exception {
        if(posInBucket <= 0 || posInList >= size){
            throw new Exception("Item doesn't exist!");
        }
        if (posInList < 0 || posInList >= this.buckets.get(posInBucket).size()) {
            throw new Exception("Invalid position given");
        }
        return this.buckets.get(posInBucket).get(posInList);
    }

    public int size() {
        return this.size;
    }

    @Override
    public String toString() {
        return "HashTable{" +
                "size=" + size +
                ", buckets=" + buckets +
                '}';
    }

    public String iterateOverElements() {
        StringBuilder res = new StringBuilder();
        for (int posInBucket = 0; posInBucket < size; posInBucket++) {
            List<T> bucket = this.buckets.get(posInBucket);
            for (int posInList = 0; posInList < bucket.size(); posInList++) {
                T element = bucket.get(posInList);
                res.append(posInBucket).append("\t|\t").append(posInList).append("\t|\t").append(element).append('\n');
                System.out.println(posInBucket + "\t|\t" + posInList + "\t|\t" + element);
            }
        }
        return res.toString();
    }
}
