# TODO: actually get better at this

defmodule Day2 do
    def part1(path) do
        File.read!(path)
        |> String.split("\r\n")
        |> Enum.filter(fn s -> s != "" end)
        |> Enum.map(&String.graphemes/1)
        |> Enum.map(&group_by_count/1)
        |> Enum.map(fn g -> {get_count(g, 2), get_count(g, 3)} end)
        |> Enum.reduce(fn {x, y}, {twos, threes} -> {twos + x, threes + y} end)
        |> multiply_tuple()
        |> IO.inspect()
    end

    defp group_by_count(xs) do
        Enum.group_by(xs, fn x -> Enum.count(xs, fn y -> x == y end) end)
    end

    defp get_count(map, key) do
        case map[key] do
            nil -> 0
            _ -> 1
        end
    end

    defp multiply_tuple({x, y}), do: x * y

   def part2(path) do
        list = File.read!(path)
            |> String.split("\r\n")
            |> Stream.filter(fn s -> s != "" end)

        list
        |> Stream.with_index()
        |> Stream.map(fn {x, i} -> get_diffs(list, {x, i}) end)
        |> Enum.find(fn d -> Enum.count(d) > 0 end)
        |> parse_result()
        |> IO.inspect()
    end

    defp get_diffs(list, {x, i}) do
        list
        |> Stream.drop(i + 1)
        |> Stream.map(fn y -> get_diff(x, y) end)
        |> Stream.filter(&diff_valid?/1)
    end

    defp get_diff(s1, s2) do
        String.myers_difference(s1, s2)
        |> Enum.group_by(fn {k, _} -> k end, fn {_, v} -> v end)
    end

    defp diff_valid?(%{:del => [del], :ins => [ins]}) do
        String.length(del) == 1 && String.length(ins) == 1
    end

    defp diff_valid?(_) do
        false
    end

    defp parse_result(xs) do
        [x | _] = Enum.take(xs, 1)
        x.eq |> Enum.join()
    end
end

path = "../inputs/day2.txt"
Day2.part1(path)
Day2.part2(path)